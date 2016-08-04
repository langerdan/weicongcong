Attribute VB_Name = "SampleColorScale"
Sub test()
    Dim row As Long, col As Long, i As Long
    row = Sheets("nli-sample-sum").UsedRange.Rows.Count
    col = Sheets("nli-sample-sum").UsedRange.Columns.Count
    For i = 2 To col
        Range(Sheets("nli-sample-sum").Cells(2, i), Sheets("nli-sample-sum").Cells(row, i)).Select
        Selection.FormatConditions.Delete
        Selection.FormatConditions.AddColorScale ColorScaleType:=3
        Selection.FormatConditions(Selection.FormatConditions.Count).SetFirstPriority
        Selection.FormatConditions(1).ColorScaleCriteria(1).Type = _
            xlConditionValueLowestValue
        With Selection.FormatConditions(1).ColorScaleCriteria(1).FormatColor
            .Color = 8109667
            .TintAndShade = 0
        End With
        Selection.FormatConditions(1).ColorScaleCriteria(2).Type = _
            xlConditionValuePercentile
        Selection.FormatConditions(1).ColorScaleCriteria(2).Value = 50
        With Selection.FormatConditions(1).ColorScaleCriteria(2).FormatColor
            .Color = 8711167
            .TintAndShade = 0
        End With
        Selection.FormatConditions(1).ColorScaleCriteria(3).Type = _
            xlConditionValueHighestValue
        With Selection.FormatConditions(1).ColorScaleCriteria(3).FormatColor
            .Color = 7039480
            .TintAndShade = 0
        End With
    Next i
End Sub

