package main

import "testing"

func TestRegexValidation(t *testing.T) {
	for _, line := range []string{"/[/", "/(?=ads)/", "@@/[/"} {
		if validate(line) == nil {
			t.Fatalf("accepted invalid Go regex: %s", line)
		}
	}
	for _, line := range []string{"/^ads[0-9]+\\.example$/", "@@||safe.example^$important"} {
		if err := validate(line); err != nil {
			t.Fatalf("rejected %s: %v", line, err)
		}
	}
}

func TestSubdomainDoesNotBlockParent(t *testing.T) {
	result, err := decisions([]string{"||ads.example.com^"}, []string{
		"example.com", "www.example.com", "ads.example.com", "a.ads.example.com",
	})
	if err != nil {
		t.Fatal(err)
	}
	expected := []bool{false, false, true, true}
	for i := range expected {
		if result[i] != expected[i] {
			t.Fatalf("decision %d: got %t want %t", i, result[i], expected[i])
		}
	}
}
