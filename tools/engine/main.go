// SPDX-License-Identifier: GPL-3.0-or-later
// The version below matches AdGuard Home v0.107.79's filtering dependency.
package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"os"
	"regexp"
	"strings"

	"github.com/AdguardTeam/urlfilter"
	"github.com/AdguardTeam/urlfilter/filterlist"
	"github.com/AdguardTeam/urlfilter/rules"
)

const engineVersion = "AdguardTeam/urlfilter v0.23.4"

func validate(line string) error {
	r, err := rules.NewNetworkRule(line, 1)
	if err != nil {
		return err
	}
	if !r.IsHostLevelNetworkRule() {
		return fmt.Errorf("not a DNS host-level rule")
	}
	pattern := strings.TrimSuffix(strings.TrimPrefix(line, "@@"), "$important")
	if strings.HasPrefix(pattern, "/") && strings.HasSuffix(pattern, "/") {
		// urlfilter compiles regex lazily and silently makes invalid patterns
		// non-matching.  Explicitly use the same Go regexp implementation here.
		_, err = regexp.Compile("(?i)" + pattern[1:len(pattern)-1])
		return err
	}
	return nil
}

func validateInput(input io.Reader) int {
	scanner := bufio.NewScanner(input)
	scanner.Buffer(make([]byte, 4096), 1024*1024)
	count, invalid, number := 0, 0, 0
	errors := []string{}
	for scanner.Scan() {
		number++
		line := strings.TrimSpace(scanner.Text())
		if line == "" || strings.HasPrefix(line, "!") || strings.HasPrefix(line, "#") {
			continue
		}
		count++
		if err := validate(line); err != nil {
			invalid++
			if len(errors) < 10 {
				errors = append(errors, fmt.Sprintf("line %d: %s: %v", number, line, err))
			}
		}
	}
	if err := scanner.Err(); err != nil {
		invalid++
		errors = append(errors, err.Error())
	}
	_ = json.NewEncoder(os.Stdout).Encode(map[string]any{
		"engine": engineVersion, "checked": count, "invalid": invalid, "errors": errors,
	})
	if invalid != 0 {
		return 1
	}
	return 0
}

func decisions(lines, hosts []string) ([]bool, error) {
	for _, line := range lines {
		if err := validate(line); err != nil {
			return nil, err
		}
	}
	list := filterlist.NewString(&filterlist.StringConfig{
		RulesText: strings.Join(lines, "\n"), ID: 1, IgnoreCosmetic: true,
	})
	storage, err := filterlist.NewRuleStorage([]filterlist.Interface{list})
	if err != nil {
		return nil, err
	}
	defer storage.Close()
	engine := urlfilter.NewDNSEngine(storage)
	result := make([]bool, len(hosts))
	for i, host := range hosts {
		res, matched := engine.Match(host)
		result[i] = matched && res.NetworkRule != nil && !res.NetworkRule.Whitelist
	}
	return result, nil
}

type matchCase struct {
	Rules []string `json:"rules"`
	Hosts []string `json:"hosts"`
}

func matchInput() int {
	var cases []matchCase
	if err := json.NewDecoder(os.Stdin).Decode(&cases); err != nil {
		fmt.Fprintln(os.Stderr, err)
		return 1
	}
	results := make([][]bool, len(cases))
	for i, c := range cases {
		var err error
		results[i], err = decisions(c.Rules, c.Hosts)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			return 1
		}
	}
	_ = json.NewEncoder(os.Stdout).Encode(results)
	return 0
}

func main() {
	match := flag.Bool("match", false, "Evaluate JSON rule/hostname cases using AdGuard DNSEngine")
	flag.Parse()
	if *match {
		os.Exit(matchInput())
	}
	os.Exit(validateInput(os.Stdin))
}
