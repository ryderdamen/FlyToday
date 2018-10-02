[![CircleCI](https://circleci.com/gh/ryderdamen/FlyToday.svg?style=shield)](https://circleci.com/gh/ryderdamen/FlyToday)
# Fly Today
[Fly today](https://ryderdamen.com/projects/fly-today) is a google assistant action that lets you know if it's VFR or IFR at an airport of your choice. For those who don't know what this means, it's pilot weather. VFR means it's Visual Flight Rules, so pilots without instrument training can fly. IFR means the weather sucks, so only pilots with specific instrument training can fly.

![Fly Today Logo](assets/banner-01.png)


## About
This project uses [aviationweather.gov](http://www.aviationweather.gov) as it's source of aviation information.

## Using it
To activate it, you can say something like this to your Google Assistant enabled device:

`````txt
Hey Google, ask Fly Today if the Weather is good at YYZ right now
`````

to which the assistant responds

`````txt
Sure, here's Fly Today.

It's looking like low IFR right now at Lester B. Pearson International, Toronto.
`````

## Project History
Originally built in PHP, I migrated this project to python so I could run it in a serverless environment and never worry about devops. It now runs as a Google Cloud Function.
