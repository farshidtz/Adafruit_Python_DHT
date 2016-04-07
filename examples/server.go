package main

import (
    "fmt"
    "net/http"
		"os/exec"
		"time"
)

func handler(w http.ResponseWriter, r *http.Request) {
	cmd := exec.Command("./AdafruitDHT.py", "11", "4")
	out, err := cmd.Output()
	if err != nil {
    fmt.Println("Error executing:", string(out), err.Error())
    return
	}
	fmt.Println(time.Now(), string(out))
		
  fmt.Fprintf(w, "<h1>~ %s</h1>", string(out))
}

func main() {
	cmd := exec.Command("./AdafruitDHT.py", "11", "4")
	out, err := cmd.Output()
	if err != nil {
    fmt.Println("Error executing:", string(out), err.Error())
    return
	}
	fmt.Println(string(out))
	
  http.HandleFunc("/", handler)
  err = http.ListenAndServe(":8080", nil)
	if err != nil {
    fmt.Println(err)
    return
	}
}