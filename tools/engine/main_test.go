package main

import (
	"reflect"
	"testing"
)

func TestActualHostScopeAndExceptions(t *testing.T) {
	p := probe{
		Rules: []string{"|exact.example.com|", "||ads.example.com^$important", "@@||safe.ads.example.com^$important"},
		Hosts: []string{"example.com", "exact.example.com", "x.exact.example.com", "ads.example.com", "x.ads.example.com", "safe.ads.example.com"},
	}
	result, err := evaluate(p)
	if err != nil {
		t.Fatal(err)
	}
	if !reflect.DeepEqual(result, []bool{false, true, false, true, true, false}) {
		t.Fatal(result)
	}
}

func TestGoRegexCannotFailSilently(t *testing.T) {
	for _, text := range []string{"/[/", "/(?=ads)/", "@@/[/"} {
		if hostRule(text) == nil {
			t.Fatal("accepted invalid regex", text)
		}
	}
	if err := hostRule("/^ads[0-9]+\\.example$/"); err != nil {
		t.Fatal(err)
	}
}
