datadir := "data"

prepare:
    mkdir -p {{datadir}}"/3dbag/source"
    mkdir -p {{datadir}}"/3dbag/jsonfg"
    mkdir -p {{datadir}}"/3dbasisvoorziening/source"
    mkdir -p {{datadir}}"/3dbasisvoorziening/jsonfg"

# Download data from the 3DBAG
download-3dbag: prepare
    #!/usr/bin/env bash
    set -euxo pipefail
    version="v20231008"
    tiles=("10-260-584" "10-262-584" "10-262-586" "10-260-586")
    download_url="https://data.3dbag.nl/"$version"/tiles"
    for tile_id in "${tiles[@]}" ;
    do
      tile_path=${tile_id//[-]//}
      tile_filename=$tile_id".city.json.gz"
      wget $download_url"/"$tile_path"/"$tile_filename -O {{datadir}}"/3dbag/source/"$tile_filename
      gunzip {{datadir}}"/3dbag/source/"$tile_filename
    done
    wget "https://data.3dbag.nl/"$version"/metadata.json" -O {{datadir}}"/3dbag/source/metadata.json"

# Download data from the 3D Basivoorziening
download-3dbasisvoorziening: prepare
    #!/usr/bin/env bash
    set -euxo pipefail
    version="2020"
    tiles=( "30gz1" )
    download_url="https://download.pdok.nl/kadaster/basisvoorziening-3d/v1_0//"$version"/volledig"
    for tile_id in "${tiles[@]}" ;
    do
      tile_filename=$tile_id"_"$version"_volledig.zip"
      wget $download_url"/"$tile_filename -O {{datadir}}"/3dbasisvoorziening/source/"$tile_filename
      unzip {{datadir}}"/3dbasisvoorziening/source/"$tile_filename -d {{datadir}}"/3dbasisvoorziening/source"
      rm {{datadir}}"/3dbasisvoorziening/source/"$tile_filename
    done

# Download sample data from the 3DBAG and 3D Basisvoorziening
download: download-3dbag download-3dbasisvoorziening

# Convert the downloaded CityJSON files to JSON-FG
convert-3dbag:
    #!/usr/bin/env bash
    set -euxo pipefail
    parallel "cityjson2jsonfg {} {{datadir}}/3dbag/jsonfg/{/.}.fg.json" ::: {{datadir}}/3dbag/source/*.city.json

convert-3dbasisvoorziening:
    #!/usr/bin/env bash
    set -euxo pipefail
    parallel --jobs 1 "cjio --suppress_msg {} upgrade save stdout | cityjson2jsonfg - {{datadir}}/3dbasisvoorziening/jsonfg/{/.}.fg.json" ::: {{datadir}}/3dbasisvoorziening/source/*.json

convert: convert-3dbag convert-3dbasisvoorziening

upload:
    rsync -aR {{datadir}}/* 3dgi-server:/var/www/3dgi-data/jsonfg
    rsync -a README_DATA.txt 3dgi-server:/var/www/3dgi-data/jsonfg/README.txt

# Remove all downloaded and converted files
clean:
    rm -rf {{datadir}}