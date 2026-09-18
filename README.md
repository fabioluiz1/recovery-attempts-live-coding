## Output

```
*********************
AS OF 0
1 EpisodeStatus.OPEN ['1'] None
*********************
AS OF 86400
1 EpisodeStatus.OPEN ['1', '4'] None
2 EpisodeStatus.OPEN ['2'] None
*********************
AS OF 172800
1 EpisodeStatus.RECOVERED ['1', '4'] 5
2 EpisodeStatus.OPEN ['2'] None
3 EpisodeStatus.OPEN ['3'] None
*********************
AS OF 259200
1 EpisodeStatus.RECOVERED ['1', '4'] 5
2 EpisodeStatus.EXPIRED ['2', '6'] None
3 EpisodeStatus.OPEN ['3'] None
```