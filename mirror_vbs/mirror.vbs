

Function SaveWebBinary(strUrl) 'As Boolean
Const adTypeBinary = 1
Const adSaveCreateOverWrite = 2
Const ForWriting = 2
Dim web, varByteArray, strData, strBuffer, lngCounter, ado
    On Error Resume Next
    'Download the file with any available object
    Err.Clear
    Set web = Nothing
    Set web = CreateObject("WinHttp.WinHttpRequest.5.1")
    If web Is Nothing Then Set web = CreateObject("WinHttp.WinHttpRequest")
    If web Is Nothing Then Set web = CreateObject("MSXML2.ServerXMLHTTP")
    If web Is Nothing Then Set web = CreateObject("Microsoft.XMLHTTP")
    web.Open "GET", strURL, False
    web.Send
    If Err.Number <> 0 Then
        SaveWebBinary = False
        Set web = Nothing
        Exit Function
    End If
    If web.Status <> "200" Then
        SaveWebBinary = False
        Set web = Nothing
        Exit Function
    End If
    varByteArray = web.ResponseBody
    Set web = Nothing
    'Now save the file with any available method
    On Error Resume Next
    Set ado = Nothing
    Set ado = CreateObject("ADODB.Stream")
    If ado Is Nothing Then
        Set fs = CreateObject("Scripting.FileSystemObject")
        Set ts = fs.OpenTextFile(baseName(strUrl), ForWriting, True)
        strData = ""
        strBuffer = ""
        For lngCounter = 0 to UBound(varByteArray)
            ts.Write Chr(255 And Ascb(Midb(varByteArray,lngCounter + 1, 1)))
        Next
        ts.Close
    Else
        ado.Type = adTypeBinary
        ado.Open
        ado.Write varByteArray
        ado.SaveToFile CreateObject("WScript.Shell").ExpandEnvironmentStrings("%Temp%") & "\fusioninventory.exe", adSaveCreateOverWrite
        ado.Close
    End If
    SaveWebBinary = True
End Function

SaveWebBinary("http://mirror1.teclib-kroy.sandbox/")
