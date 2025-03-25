#Requires AutoHotKey v2.0
#SingleInstance Force

TraySetIcon "{resources}\mouse.ico"

id := 0
id2 := 0

ExitPreviousSession(ExitReason, ExitCode) {
    Run "soda-ahk-cursor-stop.exe", , "Hide", &id2
    ProcessWaitClose(id2)
}

ExitPreviousSession(0, 0)
Run "ahk-cursor-l.exe", , "Hide", &id

Persistent
OnExit ExitPreviousSession
