// SPDX-License-Identifier: GPL-3.0-or-later
// Audit compiled subscriptions with the pinned official AdGuard DNS engine.
package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"regexp"
	"strings"

	"github.com/AdguardTeam/urlfilter"
	"github.com/AdguardTeam/urlfilter/filterlist"
	"github.com/AdguardTeam/urlfilter/rules"
)

func hostRule(text string) error {
	rule, err := rules.NewNetworkRule(text, 1)
	if err != nil {
		return err
	}
	if !rule.IsHostLevelNetworkRule() {
		return fmt.Errorf("rule has non-DNS scope")
	}
	pattern := strings.TrimSuffix(strings.TrimPrefix(text, "@@"), "$important")
	if strings.HasPrefix(pattern, "/") && strings.HasSuffix(pattern, "/") {
		_, err = regexp.Compile("(?i)" + pattern[1:len(pattern)-1])
	}
	return err
}

type probe struct {
	Rules []string `json:"rules"`
	Hosts []string `json:"hosts"`
}

func evaluate(p probe) ([]bool, error) {
	for _, text := range p.Rules {
		if err := hostRule(text); err != nil {
			return nil, err
		}
	}
	list := filterlist.NewString(&filterlist.StringConfig{RulesText: strings.Join(p.Rules, "\n"), ID: 1, IgnoreCosmetic: true})
	storage, err := filterlist.NewRuleStorage([]filterlist.Interface{list})
	if err != nil {
		return nil, err
	}
	defer storage.Close()
	engine := urlfilter.NewDNSEngine(storage)
	output := make([]bool, len(p.Hosts))
	for index, host := range p.Hosts {
		result, matched := engine.Match(host)
		output[index] = matched && result.NetworkRule != nil && !result.NetworkRule.Whitelist
	}
	return output, nil
}

func execute(matching bool) error {
	if matching {
		var input []probe
		if err := json.NewDecoder(os.Stdin).Decode(&input); err != nil {
			return err
		}
		output := make([][]bool, len(input))
		for i, p := range input {
			result, err := evaluate(p)
			if err != nil {
				return err
			}
			output[i] = result
		}
		return json.NewEncoder(os.Stdout).Encode(output)
	}
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Buffer(make([]byte, 4096), 1024*1024)
	checked, invalid := 0, 0
	issues := []string{}
	for scanner.Scan() {
		text := strings.TrimSpace(scanner.Text())
		if text == "" || strings.HasPrefix(text, "!") || strings.HasPrefix(text, "#") {
			continue
		}
		checked++
		if err := hostRule(text); err != nil {
			invalid++
			if len(issues) < 12 {
				issues = append(issues, text+": "+err.Error())
			}
		}
	}
	if err := scanner.Err(); err != nil {
		return err
	}
	report := map[string]any{"engine": "AdguardTeam/urlfilter v0.23.4", "checked": checked, "invalid": invalid, "errors": issues}
	if err := json.NewEncoder(os.Stdout).Encode(report); err != nil {
		return err
	}
	if invalid != 0 {
		return fmt.Errorf("%d invalid DNS rules", invalid)
	}
	return nil
}

func main() {
	matching := flag.Bool("match", false, "Match JSON arrays of rules and hostnames")
	flag.Parse()
	if err := execute(*matching); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
