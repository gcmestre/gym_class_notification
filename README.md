
## Description

Python script to scrap my gym page every minute and generate a ubuntu notification with are new classes available

## Install

```commandline
 git clone <this repo>

 pipenv install

```

## Run

* Open the terminal 
* Go to the project folder (.../pumpgyn)
* Enter the virtual Env
```commandline
  pipenv
```
* Run the main python script
```commandline
  python main.py
```

### Examples:

#### HTML Example of available class:
```html
[<div class="mypump-class-wrapper">
	<div class="mypump-class-hour">07:05</div>
	<!--<div class="mypump-class-title " onclick="openClassMoreInfo('#more-info-1');" >-->
	<div class="mypump-class-title"> BODY COMBAT
		<br>
			<span>45 min.</span>
			<!--<span class="mobile"></span>-->
		</br>
	</div>
	<!--<div class="mypump-class-studio desktop "></div>-->
	<div class="mypump-class-button desktop">
		<a href="javascript:void(0);" onclick="reservationMake('2e048a27-8544-4543-8f0e-a982597bd425')"> Reservar </a>
	</div>
</div>,
<div class="mypump-class-wrapper" style="background-color: #fff;">
	<div class="mypump-class-hour">19:10</div>
	<!--<div class="mypump-class-title " onclick="openClassMoreInfo('#more-info-2');" >-->
	<div class="mypump-class-title"> HIIT
		<br>
			<span>30 min.</span>
			<!--<span class="mobile"></span>-->
		</br>
	</div>
	<!--<div class="mypump-class-studio desktop "></div>-->
	<div class="mypump-class-button desktop">
		<a href="javascript:void(0);" onclick="reservationMake('06fae6cb-e2a9-4b92-8e33-e56bb4b23bbb')"> Reservar </a>
	</div>
</div>]
```

