Option Explicit

Dim WshShell, FileSystem, ScriptDirectory, RunnerPath, ExitCode
Set WshShell = CreateObject("WScript.Shell")
Set FileSystem = CreateObject("Scripting.FileSystemObject")

ScriptDirectory = FileSystem.GetParentFolderName(WScript.ScriptFullName)
RunnerPath = FileSystem.BuildPath(ScriptDirectory, "openclaw-task-runner.cmd")

' Wait=True keeps this launcher attached to the real runner. The Scheduled Task
' no longer uses VBS, but this preserves a reliable hidden manual-start option.
ExitCode = WshShell.Run("""" & RunnerPath & """", 0, True)
WScript.Quit ExitCode
