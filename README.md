# MW2MapScramblerPython

This was written with the [IW4x](https://xlabs.dev/) project in mind. 

  - [Requirements](#requirements)
  - [Arguments](#arguments)
  - [Map List Format](#map-list-format)
    - [Example](#example)

This is a small tool to randomize the map list found in the server settings file. This was very annoying for me to do by hand as it could take upwards of 10 minutes each time. IW4x does not support automatic map list scrambling so I made it myself.

Before using, please ensure that you have a map list that is in the proper format. There is a properly formatted list in this repository.

## Requirements
 - Python 3.9 or greater

## Arguments

| Argument         | Required           | Description                                                                                                                                                                                                                                              | Example                                                                                                                     |
| ---------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `MapFile`        | :heavy_check_mark: | Path to the map file. Can be relative. Goes right after script file name.                                                                                                                                                                                | ```python scrambler.py /c/MW2Server/maps.txt -l -p "mp "```, ```python scrambler.py "C:\MW2Server\maps.txt" -l -p "map "``` |
| `--ServerFile`   | :x:                | Path to server.cfg file. Can be relative.                                                                                                                                                                                                                | `--ServerFile /c/MW2Server/server.cfg`, `--ServerFile "C:\MW2Server\server.cfg"`                                            |
| `--PreArg`       | :x:                | Arguments that go before the map list. Note that spaces or new lines at the end will not be added by the script, so they must be present in the string given.                                                                                            | ```--PreArg "set sv_hostname \"IW4x Server\" set g_gametype \"war\" set sv_maprotation " ```                                |
| `--PostArg`      | :x:                | Arguments that go after the map list. Note that spaces or new lines at the beginning will not be added by the script, so they must be present in the string given.                                                                                       | See `--PreArg` example.                                                                                                     |
| `--ArgSliceChar` | :x:                | An alternative to `--PreArg` and `--PostArg`, place a character in your server.cfg file directly before and after the map list. This **CANNOT** be used with `--PreArg` **OR** `--PostArg`                                                               | `"%"`                                                                                                                       |
| `-l`, `--list`   | :x:                | Specifies if you want it output to a list file instead of to your sever.cfg file. Not to be used with `--ServerFile`. Can be used with `--Prefix` and `--PostFix` if desired. Will ignore `--ArgSliceChar` if it is present. **Option is on by default** | N/A                                                                                                                         |
| `-o`, `--override`   | :x:                | Overrides the original server.cfg with the new one. Only use this if you know what you are doing. | N/A                                                                                                                         |
| `-p`, `--prefix` | :x:                | Prefix for map names if the game requires it(e.g. mp [map name]). Spaces will not be added to the end of this string.                                                                                                                                    | `-p "mp "`                                                                                                                  |
| `-q`, `--quotes` | :x:                | Encapsulates the map list in quotes.                                                                                                                                                                                                                     | N/A                                                                                                                         |

## Map List Format

If you are making your own map list for this function, here is an example of the proper format for it to work. If you would like to know why the list must be this way then please read on, if not then look at the list below. 

The function stores the map list in two separate dicitonaries. The first, `map_list`, stores the pretty version of the map name(e.g. Afghan, Highrise, etc., etc...) as the key, with the value being the file name of the map file(e.g. mp_afghan, mp_highrise, etc., etc...), and the second, `random_map_list` stores a randomly generated index as the key, and the value is the pretty map name. This is because in Java, which this project was originally written in, dictionary access(O(1)) was significantly faster than array access(O(n)) when working with massive map lists. 

### Example

The `\n` are newlines.

`mp_afghan,Afghan\nmp_derail,Derail\nmp_estate,Estate\nmp_favela,Favela`

For a more clear example, look at `maps.txt` in the repository.