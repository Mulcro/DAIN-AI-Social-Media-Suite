import { z } from "zod";
import axios from "axios";

import {
  defineDAINService,
  ToolConfig,
} from "@dainprotocol/service-sdk";

import { CardUIBuilder, TableUIBuilder, MapUIBuilder } from "@dainprotocol/utils";

const getWeatherConfig: ToolConfig = {
  id: "get-weather",
  name: "Get Weather",
  description: "Fetches current weather for a city",
  input: z
    .object({
      locationName: z.string().describe("Location name"),
      latitude: z.number().describe("Latitude coordinate"),
      longitude: z.number().describe("Longitude coordinate"),
    })
    .describe("Input parameters for the weather request"),
  output: z
    .object({
      temperature: z.number().describe("Current temperature in Celsius"),
      windSpeed: z.number().describe("Current wind speed in km/h"),
    })
    .describe("Current weather information"),
  pricing: { pricePerUse: 0, currency: "USD" },
  handler: async ({ locationName, latitude, longitude }, agentInfo, context) => {
    console.log(
      `User / Agent ${agentInfo.id} requested weather at ${locationName} (${latitude},${longitude})`
    );


    const response = await axios.get(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current=temperature_2m,wind_speed_10m`
    );

    const { temperature_2m, wind_speed_10m } = response.data.current;
    const weatherEmoji = getWeatherEmoji(temperature_2m);

    return {
      text: `The current temperature in ${locationName} is ${temperature_2m}°C with wind speed of ${wind_speed_10m} km/h`,
      data: {
        temperature: temperature_2m,
        windSpeed: wind_speed_10m,
      },
      ui: new CardUIBuilder()
        .setRenderMode("page")
        .title(`Current Weather in ${locationName} ${weatherEmoji}`)
        .addChild(new MapUIBuilder()
          .setInitialView(latitude, longitude, 10)
          .setMapStyle('mapbox://styles/mapbox/streets-v12')
          .addMarkers([
            {
              latitude,
              longitude,
              title: locationName,
              description: `Temperature: ${temperature_2m}°C\nWind: ${wind_speed_10m} km/h`,
              text: `${locationName} ${weatherEmoji}`,
            }
          ])
          .build())
        .content(`Temperature: ${temperature_2m}°C\nWind Speed: ${wind_speed_10m} km/h`)
        .build(),
    };
  },
};

const dainService = defineDAINService({
  metadata: {
    title: "Weather DAIN Service",
    description:
      "A DAIN service for current weather and forecasts using Open-Meteo API",
    version: "1.0.0",
    author: "Your Name",
    tags: ["weather", "forecast", "dain"],
    logo: "https://cdn-icons-png.flaticon.com/512/252/252035.png"
  },
  identity: {
    apiKey: process.env.DAIN_API_KEY,
  },
  tools: [getWeatherConfig, getWeatherForecastConfig],
});

dainService.startNode().then(({ address }) => {
  console.log("DAIN Service is running at :" + address().port);
});

