# cassini_2021_nature_discoverer

A repo for work completed during the June 18-20, 2021 CASSINI Hackathon sponsored by the ESA. [Link](https://www.dropbox.com/s/asukt2jkcr1t4kc/Nature%20Discoverer%20-%20Cassini%202021%20-%20Sunday%20Afternoon.pdf?dl=1) to brief presentation.

## Example

**Valais Canton geotiff colorized** - Sentinel 2

![valais colorized](https://user-images.githubusercontent.com/74869040/122691268-ef4c0f80-d22e-11eb-879e-70c46b79b8e7.png)

**Valais Canton geotiff - <font color="red">Areas of Interest Overlaid</font>** - Sentinel 2

![valais + areas of interest (prelim)](https://user-images.githubusercontent.com/74869040/122691284-00951c00-d22f-11eb-9b81-cbd8b5c910de.jpeg)

- *Areas of interest are highlighted in red vs. the green/yellow/blue colormap for "normal" terrain*

## Overview

What if traveling to new places could be reliably engaging and rewarding? 

Idea is to use visual (RGB layers) for [remote sensing](https://earthdata.nasa.gov/learn/backgrounders/remote-sensing) / identification of outdoor recreation areas and points of interest. A neural network model (finalization TBD) would suggest potential "new" areas, and users would be engaged / shown these recommendations through an app that tailors recs to user interests. Users would also be further engaged through AR experiences on the app.

### Main Features
1. Recommend potential outdoor recreation locations (remote sensing with Sentinel-2)
2. Keep customers engaged with the outdoors (AR experience)
### Value proposition:
1. Cantons or other government entities looking to increase tourism
2. Outdoor recreation outfitters / magazines: sell as a service

## Data Sources

- Sentinel-2 geospatial data (can be accessed [here](https://scihub.copernicus.eu/)
- Points of interest exported and overlaid from OpenStreetMap via [HOT Export Tool](https://export.hotosm.org/en/v3/learn/quick_start)
- Lat/Long of climbing areas from [TheCrag](https://www.thecrag.com/en/climbing/switzerland/alpen/wallis)
- [geojson](http://geojson.io) for custom shape drawing / adding

## TODO / Roadmap

1. generate full dataset with overlaid areas of interest (matplotlib savefigure issue)
2. reformat training data to text labels, select model (CNN or YOLOv5, or other)
3. select and train model
4. Augment results in app with SwissTOPO data 
5. Polish AR experience

