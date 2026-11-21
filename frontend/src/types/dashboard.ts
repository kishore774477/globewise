export type GlobeWiseLocation = {
  name: string;
  admin1?: string;
  country: string;
  country_code: string;
  latitude: number;
  longitude: number;
  timezone?: string;
  population?: number;
};

export type WeatherData = {
  temperature: number | null;
  feels_like: number | null;
  condition: string;
  humidity: number | null;
  wind_speed: number | null;
  precipitation: number | null;
  source: string;
  daily: {
    dates: string[];
    max_temperature: number[];
    min_temperature: number[];
    rain_probability: number[];
  };
};

export type CountryInfo = {
  name: string;
  capital: string;
  currency_code: string;
  currency_name: string;
  languages: string[];
  region: string;
  subregion: string;
  population: number | null;
  timezones: string[];
  flag: string;
  source: string;
};

export type CurrencyData = {
  amount: number;
  from_currency: string;
  to_currency: string;
  rate: number | null;
  converted_amount: number | null;
  source: string;
};

export type EarthquakeData = {
  title: string;
  place: string;
  magnitude: number;
  url: string;
  time: number;
  distance_km: number;
  depth_km: number;
};

export type SafetyData = {
  level: string;
  score: number;
  reasons: string[];
  nearby_earthquakes: EarthquakeData[];
};

export type DashboardData = {
  location: GlobeWiseLocation;
  weather: WeatherData;
  country_info: CountryInfo;
  currency: CurrencyData;
  safety: SafetyData;
  ai_tip: string;
};
