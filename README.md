# README.MD


main.py # takes care setup/initializing different loops (logging coalation?)
  |
  |- thermal.py # thermal detection loop
  |       |
  |       |- thermal_camera.py # captures camera object and does preprocessing
  |
  |- visible.py # visible light smoke/flame detection loop
  |       | 
  |       |- visible.py # captures visible camera object and does preprocessing
  |
  |- mavlink.py # mavlink connection loop
  |       |
  |       |-mavlink_functions.py # aircraft control functions ie. fly to x
  |
  |- logger.py # does logging data processing
  | 
  |- CO2_sensor.py # future CO2/gas sensor loop
  |
  |- additional modules...


This will probably be refactored into C/Rust/Zig in the future as I learn one of these languages.

Performance is the main goal here, I want this all to be able to run on a rasberry Pi 4 with 2gb of ram. The key thing is not using a ML model or Neural network for any detection. This means that some interesting techniques will have to be used for the visible light smoke detection. I have a few ideas.
