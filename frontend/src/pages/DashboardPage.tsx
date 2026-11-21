import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import {
  CloudSun,
  ShieldCheck,
  Wallet,
  Sparkles,
  MapPin,
  RefreshCw,
  Search,
  Globe2,
  Activity,
  Compass,
  Thermometer,
  Wind,
  Droplets,
  AlertTriangle,
} from "lucide-react";

import { getDashboardData } from "../services/dashboardApi";
import type { DashboardData } from "../types/dashboard";

export default function DashboardPage() {
  const [cityInput, setCityInput] = useState("Hosur");
  const [activeCity, setActiveCity] = useState("Hosur");
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeSection, setActiveSection] = useState("dashboard");

  // Fetches data and updates state only after the request settles, so it is
  // safe to call from an effect.
  async function fetchDashboard(city: string) {
    try {
      const dashboardData = await getDashboardData(city);

      setData(dashboardData);
      setActiveCity(city);
      setError("");
    } catch (err) {
      console.error("Dashboard load error:", err);
      setError("Unable to load live GlobeWise data. Check backend terminal and internet connection.");
    } finally {
      setLoading(false);
    }
  }

  function loadDashboard(city: string) {
    setLoading(true);
    setError("");
    void fetchDashboard(city);
  }

  function handleSearch(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedCity = cityInput.trim();

    if (trimmedCity.length < 2) {
      setError("Enter a valid city name.");
      return;
    }

    loadDashboard(trimmedCity);
  }

  useEffect(() => {
    // Initial load. State is only updated inside promise callbacks, and the
    // initial state already has loading=true.
    let cancelled = false;

    getDashboardData("Hosur")
      .then((dashboardData) => {
        if (!cancelled) setData(dashboardData);
      })
      .catch((err) => {
        console.error("Dashboard load error:", err);
        if (!cancelled) {
          setError("Unable to load live GlobeWise data. Check backend terminal and internet connection.");
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  function scrollToSection(sectionId: string) {
    setActiveSection(sectionId);

    document.getElementById(sectionId)?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  }

  const locationName = data?.location?.name ?? activeCity;
  const locationCountry = data?.location?.country ?? "Unknown";
  const locationRegion = data?.location?.admin1 ?? "";
  const weather = data?.weather;
  const safety = data?.safety;
  const currency = data?.currency;
  const countryInfo = data?.country_info;

  return (
    <main className="dashboard-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">🌍</div>
          <div>
            <strong>GlobeWise</strong>
            <span>Travel Intelligence</span>
          </div>
        </div>

        <nav>
          <button
            className={activeSection === "dashboard" ? "active" : ""}
            onClick={() => scrollToSection("dashboard")}
          >
            Dashboard
          </button>

          <button
            className={activeSection === "weather" ? "active" : ""}
            onClick={() => scrollToSection("weather")}
          >
            Weather
          </button>

          <button
            className={activeSection === "safety" ? "active" : ""}
            onClick={() => scrollToSection("safety")}
          >
            Safety
          </button>

          <button
            className={activeSection === "currency" ? "active" : ""}
            onClick={() => scrollToSection("currency")}
          >
            Currency
          </button>

          <button
            className={activeSection === "country" ? "active" : ""}
            onClick={() => scrollToSection("country")}
          >
            Country
          </button>

          <button
            className={activeSection === "ai-guide" ? "active" : ""}
            onClick={() => scrollToSection("ai-guide")}
          >
            AI Guide
          </button>
        </nav>

        <div className="sidebar-footer">
          <p>Live API Mode</p>
          <strong>{loading ? "Syncing..." : "Connected"}</strong>
        </div>
      </aside>

      <section className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">Personal Global Life Assistant</p>
            <h1>GlobeWise Command Center</h1>
          </div>

          <button
            className="refresh-button"
            disabled={loading}
            onClick={() => loadDashboard(cityInput.trim() || activeCity)}
          >
            <RefreshCw size={18} className={loading ? "spin" : ""} />
            {loading ? "Refreshing" : "Refresh"}
          </button>
        </header>

        <section id="dashboard" className="hero-panel">
          <div>
            <div className="status-pill">
              <Compass size={16} />
              Live city intelligence
            </div>

            <h2>
              Explore safety, weather, country and currency insights for any city.
            </h2>

            <form className="search-box" onSubmit={handleSearch}>
              <Search size={20} />
              <input
                value={cityInput}
                onChange={(event) => setCityInput(event.target.value)}
                placeholder="Search city, example: Chennai, Dubai, Tokyo"
              />
              <button type="submit" disabled={loading}>
                {loading ? "Loading..." : "Analyze"}
              </button>
            </form>

            {error && <p className="inline-error">{error}</p>}
          </div>

          <div className="city-card">
            <MapPin size={24} />
            <h3>{locationName}</h3>
            <p>
              {locationRegion ? `${locationRegion}, ` : ""}
              {locationCountry}
            </p>
            <span>{data?.location?.timezone ?? "Timezone unknown"}</span>
          </div>
        </section>

        <section className="metric-grid">
          <article id="weather" className="metric-card weather-card">
            <div className="card-top">
              <div className="icon-box weather">
                <CloudSun size={24} />
              </div>
              <span>{weather?.source ?? "Open-Meteo"}</span>
            </div>

            <p className="card-label">Weather Now</p>
            <h3>{weather?.temperature ?? "-"}°C</h3>
            <p>{weather?.condition ?? "Weather unavailable"}</p>

            <div className="mini-stats">
              <div>
                <Thermometer size={16} />
                Feels {weather?.feels_like ?? "-"}°C
              </div>
              <div>
                <Wind size={16} />
                Wind {weather?.wind_speed ?? "-"} km/h
              </div>
              <div>
                <Droplets size={16} />
                Humidity {weather?.humidity ?? "-"}%
              </div>
            </div>
          </article>

          <article id="safety" className="metric-card">
            <div className="card-top">
              <div className="icon-box safety">
                <ShieldCheck size={24} />
              </div>
              <span>Risk Engine</span>
            </div>

            <p className="card-label">Safety Score</p>
            <h3>{safety?.level ?? "Unknown"}</h3>
            <p>Risk score: {safety?.score ?? 0}/100</p>

            <div className="risk-bar">
              <div style={{ width: `${safety?.score ?? 0}%` }} />
            </div>

            <small>{safety?.reasons?.[0] ?? "No safety reason available."}</small>
          </article>

          <article id="currency" className="metric-card">
            <div className="card-top">
              <div className="icon-box currency">
                <Wallet size={24} />
              </div>
              <span>{currency?.source ?? "Frankfurter"}</span>
            </div>

            <p className="card-label">Currency</p>
            <h3>
              {currency?.from_currency ?? "-"} → {currency?.to_currency ?? "-"}
            </h3>
            <p>
              {currency?.rate
                ? `1 ${currency.from_currency} = ${currency.rate} ${currency.to_currency}`
                : "Rate unavailable"}
            </p>
            <small>
              Converted: {currency?.converted_amount ?? "-"} {currency?.to_currency ?? ""}
            </small>
          </article>
        </section>

        <section className="content-grid">
          <article id="ai-guide" className="large-panel">
            <div className="panel-heading">
              <div className="icon-box ai">
                <Sparkles size={22} />
              </div>
              <div>
                <p className="card-label">AI Travel Insight</p>
                <h3>What you should know</h3>
              </div>
            </div>

            <p className="ai-text">
              {data?.ai_tip ?? "AI guidance unavailable right now."}
            </p>

            <div className="advice-grid">
              <div>
                <AlertTriangle size={18} />
                <strong>Safety</strong>
                <span>{safety?.level ?? "Unknown"} risk right now</span>
              </div>
              <div>
                <CloudSun size={18} />
                <strong>Weather</strong>
                <span>{weather?.condition ?? "Unknown"}</span>
              </div>
              <div>
                <Activity size={18} />
                <strong>Earthquake</strong>
                <span>{safety?.nearby_earthquakes?.length ?? 0} nearby alerts</span>
              </div>
            </div>
          </article>

          <article id="country" className="side-panel">
            <div className="panel-heading">
              <div className="icon-box country">
                <Globe2 size={22} />
              </div>
              <div>
                <p className="card-label">Country Intelligence</p>
                <h3>{countryInfo?.name ?? locationCountry}</h3>
              </div>
            </div>

            <ul className="info-list">
              <li>
                <span>Capital</span>
                <strong>{countryInfo?.capital ?? "Unknown"}</strong>
              </li>
              <li>
                <span>Region</span>
                <strong>{countryInfo?.region ?? "Unknown"}</strong>
              </li>
              <li>
                <span>Currency</span>
                <strong>{countryInfo?.currency_code ?? "Unknown"}</strong>
              </li>
              <li>
                <span>Languages</span>
                <strong>{countryInfo?.languages?.slice(0, 2).join(", ") || "Unknown"}</strong>
              </li>
            </ul>
          </article>
        </section>

        <section className="forecast-panel">
          <div className="panel-heading">
            <div className="icon-box weather">
              <CloudSun size={22} />
            </div>
            <div>
              <p className="card-label">7-Day Forecast</p>
              <h3>Weather trend</h3>
            </div>
          </div>

          <div className="forecast-row">
            {(weather?.daily?.dates ?? []).slice(0, 7).map((date, index) => (
              <div className="forecast-day" key={date}>
                <span>{new Date(date).toLocaleDateString("en-US", { weekday: "short" })}</span>
                <strong>{weather?.daily?.max_temperature?.[index] ?? "-"}°</strong>
                <small>{weather?.daily?.min_temperature?.[index] ?? "-"}° min</small>
                <em>{weather?.daily?.rain_probability?.[index] ?? 0}% rain</em>
              </div>
            ))}
          </div>
        </section>

        <section className="earthquake-panel">
          <div className="panel-heading">
            <div className="icon-box quake">
              <Activity size={22} />
            </div>
            <div>
              <p className="card-label">Safety Monitoring</p>
              <h3>Nearby earthquake activity</h3>
            </div>
          </div>

          {safety?.nearby_earthquakes?.length ? (
            <div className="quake-items">
              {safety.nearby_earthquakes.map((quake) => (
                <a key={`${quake.title}-${quake.time}`} href={quake.url} target="_blank" rel="noreferrer">
                  <strong>{quake.title}</strong>
                  <span>{quake.distance_km} km away</span>
                </a>
              ))}
            </div>
          ) : (
            <p className="muted">No nearby significant earthquake activity detected.</p>
          )}
        </section>
      </section>
    </main>
  );
}

