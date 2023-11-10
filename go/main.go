package main

import (
	"bufio"
	_ "embed"
	"io/ioutil"
	"log"
	"os"
	"sort"
	"strings"

	"github.com/fatih/color"
	"github.com/rodaine/table"
)

//go:embed ncnn_layer.csv
var layerData string

func main() {
	// log.SetFlags(log.Lshortfile | log.LstdFlags)
	layerLines := strings.Split(layerData, "\n")
	dict := make(map[string][]string)
	for _, line := range layerLines[1:] {
		cols := strings.Split(line, ",")
		if len(cols) == 7 {
			dict[cols[0]] = []string{
				cols[1],
				cols[2],
				cols[3],
				cols[4],
				cols[5],
				strings.TrimSuffix(cols[6], "\r"),
			}
		}
	}
	if len(os.Args) != 2 {
		log.Fatal("--Usage: ncnninfo ncnn.param")
	}
	content, err := ioutil.ReadFile(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}
	paramLines := strings.Split(string(content), "\n")
	counts := make(map[string]int)
	for _, line := range paramLines[2:] {
		scanner := bufio.NewScanner(strings.NewReader(line))
		scanner.Split(bufio.ScanWords)
		if scanner.Scan() {
			counts[scanner.Text()]++
		}
	}

	var opNames []string
	for op := range counts {
		if op == "Input" {
			continue
		}
		opNames = append(opNames, op)
	}
	sort.Slice(opNames, func(i, j int) bool {
		return counts[opNames[i]] > counts[opNames[j]]
	})

	headerFmt := color.New(color.FgGreen, color.Underline).SprintfFunc()
	columnFmt := color.New(color.FgYellow).SprintfFunc()

	table := table.New("Op.", "Total", "arm", "loongarch", "mips", "riscv", "vulkan", "x86")
	table.WithHeaderFormatter(headerFmt).WithFirstColumnFormatter(columnFmt)
	for _, op := range opNames {
		row := dict[op]
		if len(row) == 0 {
			table.AddRow(op, counts[op], "x", "x", "x", "x", "x", "x")
		} else {
			table.AddRow(op, counts[op], compare(row[0]), compare(row[1]), compare(row[2]), compare(row[3]), compare(row[4]), compare(row[5]))
		}
	}
	table.Print()
}

func compare(status string) string {
	if status == "1" {
		return "Y"
	}
	return ""
}
