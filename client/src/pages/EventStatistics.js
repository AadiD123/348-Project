import React, { useState, useEffect } from "react";
import axios from "axios";

const EventStatistics = () => {
  const [categories, setCategories] = useState([]);
  const [bars, setBars] = useState([]);
  const [statistics, setStatistics] = useState(null); // Store aggregated statistics
  const [filters, setFilters] = useState({
    start_date: "",
    end_date: "",
    category: "",
    bar_id: "",
  });
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetchBars();
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await axios.get("/categories");
      setCategories(response.data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  const fetchBars = async () => {
    try {
      const response = await axios.get("/bars");
      setBars(response.data);
    } catch (error) {
      console.error("Error fetching bars:", error);
    }
  };

  const fetchEvents = async () => {
    try {
      const response = await axios.get("/event-stats", { params: filters });
      setStatistics(response.data); // Update statistics state with API response
      const response2 = await axios.get("/filtered-events", {
        params: filters,
      });
      setEvents(response2.data);
    } catch (error) {
      console.error("Error fetching event statistics:", error);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters((prevFilters) => ({
      ...prevFilters,
      [name]: value,
    }));
  };

  return (
    <div className="container mx-auto p-5">
      <h1 className="text-center text-3xl font-bold mb-6">Event Statistics</h1>
      <div className="flex w-full justify-between text-center">
        <div>
          <label className="block mb-1 font-semibold">Start Date</label>
          <input
            type="date"
            name="start_date"
            value={filters.start_date}
            onChange={handleFilterChange}
            className="w-full px-3 py-2 pr-10 rounded border border-gold text-gold"
          />
        </div>
        <div>
          <label className="block mb-1 font-semibold">End Date</label>
          <input
            type="date"
            name="end_date"
            value={filters.end_date}
            onChange={handleFilterChange}
            className="w-full px-3 py-2 pr-10 rounded border border-gold text-gold"
          />
        </div>
        <div>
          <label className="block mb-1 font-semibold">Event Category</label>
          <select
            name="category"
            value={filters.category}
            onChange={handleFilterChange}
            className="px-3 py-2 rounded border border-gold"
          >
            <option value="">Select an option</option>
            {categories.map((category) => (
              <option key={category.category_id} value={category.name}>
                {category.name}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="block mb-1 font-semibold">Bar Name</label>
          <select
            name="bar_id"
            value={filters.bar_id}
            onChange={handleFilterChange}
            className="w-full px-3 py-2 rounded border border-gold"
          >
            <option value="">Select a bar</option>
            {bars.map((bar) => (
              <option key={bar.bar_id} value={bar.bar_id}>
                {bar.name}
              </option>
            ))}
          </select>
        </div>{" "}
        <button
          onClick={fetchEvents}
          className="mt-4 px-4 py-2 bg-gold text-white rounded"
        >
          Fetch Statistics
        </button>
      </div>

      {statistics && (
        <div>
          <div className="mt-6">
            <h2 className="text-2xl font-bold mb-4">Statistics</h2>
            <p>
              <strong>Average Cover Charge:</strong> $
              {statistics.average_cover_charge}
            </p>
            <p>
              <strong>Average Duration:</strong>{" "}
              {statistics.average_duration_minutes} minutes
            </p>
            <p>
              <strong>Average Age Requirement:</strong>{" "}
              {statistics.average_age_requirement}
            </p>
            <p>
              <strong>Average Event Start Time:</strong>{" "}
              {statistics.average_event_time}
            </p>
          </div>
          <div className="grid grid-cols-3 gap-4 mt-10">
            {events.map((event) => (
              <div
                key={event.event_id}
                className="bg-black text-gold p-4 rounded-lg mb-4 shadow-lg"
              >
                <h2 className="text-2xl font-semibold">{event.title}</h2>
                <p className="text-sm">{event.name}</p>
                <p>{event.description}</p>
                <p className="text-sm mt-2">{event.age_requirement}+</p>
                <p className="text-sm">Cover Charge: ${event.cover_charge}</p>
                <p className="text-sm mt-2">{event.event_date}</p>
                <p className="text-sm">
                  {event.start_time} - {event.end_time}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default EventStatistics;
