package main

import (
	"C"
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"strings"
)

type result struct {
	MatchedLines []struct {
		LineNumber int
		Line       string
	}
	Error string
}

func SearchStringInFile(filePath, searchString string) *C.char {
	file, err := os.Open(filePath)
	if err != nil {
		res := result{Error: fmt.Sprintf("Failed to open file: %s", filePath)}
		jsonRes, _ := json.Marshal(res)
		return C.CString(string(jsonRes))
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	matchedLines := make([]struct {
		LineNumber int
		Line       string
	}, 0)

	lineNumber := 0
	for scanner.Scan() {
		lineNumber++
		line := scanner.Text()
		if strings.Contains(line, searchString) {
			matchedLines = append(matchedLines, struct {
				LineNumber int
				Line       string
			}{
				LineNumber: lineNumber,
				Line:       line,
			})
		}
	}

	if err := scanner.Err(); err != nil {
		res := result{Error: fmt.Sprintf("Failed to read file: %s", filePath)}
		jsonRes, _ := json.Marshal(res)
		return C.CString(string(jsonRes))
	}
	res := result{MatchedLines: matchedLines}
	jsonRes, err := json.Marshal(res)
	if err != nil {
		return C.CString("")
	}

	return C.CString(string(jsonRes))
}

//export searchStringInFileWrapper
func searchStringInFileWrapper(cFilePath *C.char, cSearchString *C.char) *C.char {
	filePath := C.GoString(cFilePath)
	searchString := C.GoString(cSearchString)
	return SearchStringInFile(filePath, searchString)
}

func main() {
}
