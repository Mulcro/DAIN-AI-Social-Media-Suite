# DAIN-AI-Social-Media-Suite
 A service that provides AI assisted capabilities to content creation

## How to run Locally

***PREREQUISITE:*** Make sure you have node.js installed & create DAIN account [here](https://beachhacks-platform.dain.org/)

If not do so following [these](https://nodejs.org/en/download) instructions

### Step 1

 Follow [these](https://beachhacks-docs.dain.org/docs/getting-started/services/project-setup) instructions to retrieve your API key


### Step 2

 Create .env & .env.development files and copy your api key into DAIN_API_KEY field
 
 ```bash
 touch .env .env.development
 ```
 
 The structure of your .env should look like this
 ```sh
 DAIN_API_KEY= Your API Key
 ```
 
 The structure of your .env.development should look like this
 ```sh
 DAIN_API_KEY= Your API Key
 PORT=
 ```

### Step 3

 Install dependencies. Make sure you're in root directory
 
 ```bash
 npm i
 ```

### Step 4

 Deploy and run the app
 
 - deploy
 ```bash
 dain build
 dain deploy
 ```
 - run
 ```bash
 dain dev
 ```

 ***Note:*** Keep track of your tunnel url once you've ran the dev script

### Step 5

 Follow [these](https://beachhacks-docs.dain.org/docs/getting-started/services/test-out) steps to connect your local instance to the DAIN assistant (See DAIN assistant [here](https://beachhacks-assistant.dain.org/))

