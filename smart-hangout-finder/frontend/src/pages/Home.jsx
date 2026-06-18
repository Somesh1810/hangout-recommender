import { useState } from "react";
import API from "../services/api";
import MapView from "../components/MapView";

export default function Home() {
  const [lat, setLat] = useState(null);
  const [lon, setLon] = useState(null);

  const [places, setPlaces] = useState([]);
  const [occasion, setOccasion] = useState("friends");

  const [budget, setBudget] = useState(1000);
  const [cuisine, setCuisine] = useState("");
  const [ambience, setAmbience] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const findPlaces = async () => {

    setLoading(true);
    setError("");

    try {

      const response = await API.get("/places", {
        params: {
          lat: lat || 12.9716,
          lon: lon || 77.5946,
          radius: 30000,

          occasion,
          budget,
          cuisine,
          ambience
        }
      });

      console.log(response.data);

      setPlaces(
        response.data.recommendations || []
      );

    } catch (err) {

      console.error(err);

      setError(
        "Failed to fetch recommendations"
      );

    } finally {

      setLoading(false);

    }

  };

  return (

    <div className="min-h-screen bg-slate-900 text-white p-8">

      <div className="max-w-7xl mx-auto">

        <h1 className="text-5xl font-bold mb-3">
          Smart Hangout Finder 🚀
        </h1>

        <p className="text-slate-400 mb-8">
          Find the best places based on
          occasion, budget, cuisine,
          and ambience.
        </p>

        {/* Filters */}

        <div className="flex flex-wrap gap-4 mb-8">

          {/* Occasion */}

          <select
            value={occasion}
            onChange={(e) =>
              setOccasion(
                e.target.value
              )
            }
            className="
            text-black
            px-4
            py-2
            rounded-lg
            "
          >
            <option value="friends">
              Friends
            </option>

            <option value="date">
              Date
            </option>

            <option value="family">
              Family
            </option>

            <option value="work">
              Work
            </option>

            <option value="solo">
              Solo
            </option>

          </select>

          {/* Budget */}

          <select
            value={budget}
            onChange={(e) =>
              setBudget(
                Number(
                  e.target.value
                )
              )
            }
            className="
            text-black
            px-4
            py-2
            rounded-lg
            "
          >
            <option value={500}>
              ₹500
            </option>

            <option value={1000}>
              ₹1000
            </option>

            <option value={1500}>
              ₹1500
            </option>

            <option value={2000}>
              ₹2000
            </option>

            <option value={3000}>
              ₹3000
            </option>

          </select>

          {/* Cuisine */}

          <select
            value={cuisine}
            onChange={(e) =>
              setCuisine(
                e.target.value
              )
            }
            className="
            text-black
            px-4
            py-2
            rounded-lg
            "
          >
            <option value="">
              Any Cuisine
            </option>

            <option value="coffee">
              Coffee
            </option>

            <option value="indian">
              Indian
            </option>

            <option value="asian">
              Asian
            </option>

            <option value="fusion">
              Fusion
            </option>

            <option value="south_indian">
              South Indian
            </option>

          </select>

          {/* Ambience */}

          <select
            value={ambience}
            onChange={(e) =>
              setAmbience(
                e.target.value
              )
            }
            className="
            text-black
            px-4
            py-2
            rounded-lg
            "
          >
            <option value="">
              Any Ambience
            </option>

            <option value="quiet">
              Quiet
            </option>

            <option value="party">
              Party
            </option>

            <option value="work">
              Work Friendly
            </option>

            <option value="family">
              Family
            </option>

            <option value="date">
              Romantic
            </option>

          </select>

          {/* Button */}
          <button
            onClick={() => {

              navigator.geolocation.getCurrentPosition(

                (position) => {

                  setLat(
                    position.coords.latitude
                  );

                  setLon(
                    position.coords.longitude
                  );

                  alert("Location Updated");

                },

                (error) => {

                  console.error(error);

                  alert(
                    "Unable to get location"
                  );

                }

              );

            }}
            className="
            bg-green-600
            px-5
            py-2
            rounded
            "
          >
            Use My Location
          </button>  
            
          
          <button
            onClick={findPlaces}
            disabled={loading}
            className="
            bg-blue-600
            hover:bg-blue-700
            px-6
            py-2
            rounded-lg
            "
          >
            {loading
              ? "Searching..."
              : "Find Places"}
          </button>

        </div>

        {/* Error */}

        {error && (

          <div
            className="
            bg-red-500/20
            border
            border-red-500
            p-3
            rounded-lg
            mb-6
            "
          >
            {error}
          </div>

        )}

        <p className="mb-4 text-cyan-400">

          Current Location:

          {" "}

          {lat
            ? `${lat.toFixed(4)},
            ${lon.toFixed(4)}`
            : "Using Bangalore Default"}

        </p>
        {/* Result Count */}

        <p className="
        text-green-400
        font-semibold
        mb-6
        ">
          Results Found:
          {" "}
          {places.length}
        </p>

        {/* Cards */}

        <div
          className="
          grid
          md:grid-cols-2
          lg:grid-cols-3
          gap-6
          "
        >
          <div className="mt-10">

            <MapView
              places={places}
            />

        </div>

          {places.map(
            (place, index) => (

              <div
                key={index}
                className="
                bg-slate-800
                p-5
                rounded-xl
                shadow-lg
                "
              >

                <h2
                  className="
                  text-xl
                  font-bold
                  mb-3
                  "
                >
                  {place.name}
                </h2>

                <p>
                  🍽️ Type:
                  {" "}
                  {place.type}
                </p>

                <p>
                  📍 Distance:
                  {" "}
                  {place.distance_km}
                  {" "}
                  km
                </p>

                <p>
                  ⭐ Score:
                  {" "}
                  {place.score}
                </p>

                <p>
                  🥘 Cuisine:
                  {" "}
                  {place.cuisine}
                </p>

                <p>
                  💰 Budget:
                  {" "}
                  ₹{place.budget}
                </p>

                <p>
                  🎯 Ambience:
                  {" "}
                  {place.ambience?.join(", ")}
                </p>

                <a
                  href={`https://www.google.com/maps?q=${place.lat},${place.lon}`}
                  target="_blank"
                  rel="noreferrer"
                  className="
                  inline-block
                  mt-4
                  bg-green-600
                  hover:bg-green-700
                  px-4
                  py-2
                  rounded-lg
                  "
                >
                  Open in Maps
                </a>

              </div>

            )
          )}

        </div>

      </div>

    </div>

  );

}