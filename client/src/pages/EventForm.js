import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useParams } from "react-router-dom";

const EventForm = () => {
  const [bars, setBars] = useState([]);
  const [categories, setCategories] = useState([]);
  const [eventData, setEventData] = useState({
    bar_id: "",
    title: "",
    description: "",
    event_date: "",
    start_time: "",
    end_time: "",
    cover_charge: "",
    age_requirement: "",
    category_id: "",
  });

  const eventId = useParams().eventId; // Get eventId from URL params

  useEffect(() => {
    fetchBars();
    fetchCategories();
    if (eventId) {
      fetchEvent(eventId); // Fetch event details if editing
    }
  }, [eventId]);

  const fetchBars = async () => {
    try {
      const response = await axios.get("/bars");
      setBars(response.data);
    } catch (error) {
      console.error("Error fetching bars:", error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.get("/categories");
      setCategories(response.data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  // Fetch event data if eventId is provided (for editing)
  const fetchEvent = async (eventId) => {
    try {
      const response = await axios.get(`/events/${eventId}`);
      setEventData(response.data); // Pre-populate form fields with event data
    } catch (error) {
      console.error("Error fetching event:", error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEventData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (eventId) {
        // Edit event
        await axios.put(`/events/${eventId}`, eventData);
      } else {
        // Add new event
        await axios.post("/events", eventData);
      }
      window.location.href = "/"; // Redirect to event list page
    } catch (error) {
      console.error("Error submitting event:", error);
    }
  };

  return (
    <div className="container mx-auto p-5">
      <h1 className="text-center text-3xl font-bold mb-6">
        {eventId ? "Edit Event" : "Create Event"}
      </h1>
      <form onSubmit={handleSubmit} className="space-y-4 p-10 bg-gray-900">
        {/* Event Title */}
        <div>
          <label className="block mb-1 font-semibold text-gold">
            Event Title
          </label>
          <input
            type="text"
            name="title"
            value={eventData.title}
            onChange={handleInputChange}
            className="w-full px-3 py-2 rounded border border-gold bg-black text-gold"
            required
          />
        </div>

        {/* Select Bar */}
        <div>
          <label className="block mb-1 font-semibold text-gold">
            Select Bar
          </label>
          <select
            name="bar_id"
            value={eventData.bar_id}
            onChange={handleInputChange}
            className="w-full px-3 py-2 rounded border border-gold bg-black text-gold"
            required
          >
            <option value="">Select a bar</option>
            {bars.map((bar) => (
              <option key={bar.bar_id} value={bar.bar_id}>
                {bar.name}
              </option>
            ))}
          </select>
        </div>

        {/* Description */}
        <div>
          <label className="block mb-1 font-semibold text-gold">
            Description
          </label>
          <textarea
            name="description"
            value={eventData.description}
            onChange={handleInputChange}
            className="w-full px-3 py-2 rounded border border-gold bg-black text-gold"
            required
          />
        </div>

        {/* Cover Charge and Age Requirement */}
        <div className="grid grid-cols-2 gap-5">
          <div>
            <label className="block mb-1 font-semibold text-gold">
              Cover Charge ($)
            </label>
            <input
              type="number"
              name="cover_charge"
              value={eventData.cover_charge}
              onChange={handleInputChange}
              className="w-full px-3 py-2 rounded border border-gold bg-black text-gold"
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-semibold text-gold">
              Age Requirement
            </label>
            <input
              type="number"
              name="age_requirement"
              value={eventData.age_requirement}
              onChange={handleInputChange}
              className="w-full px-3 py-2 rounded border border-gold bg-black text-gold"
              required
            />
          </div>
        </div>

        {/* Select Category and Event Date */}
        <div className="grid grid-cols-2 gap-5">
          <div>
            <label className="block mb-1 font-semibold text-gold">
              Select Category
            </label>
            <select
              name="category_id"
              value={eventData.category_id}
              onChange={handleInputChange}
              className="w-full px-3 py-2 rounded border border-gold bg-black text-gold"
              required
            >
              <option value="">Select a category</option>
              {categories.map((category) => (
                <option key={category.category_id} value={category.category_id}>
                  {category.name}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block mb-1 font-semibold text-gold">
              Event Date
            </label>
            <input
              type="date"
              name="event_date"
              value={eventData.event_date}
              onChange={handleInputChange}
              className="w-full px-3 py-2 rounded border border-gold bg-black text-gold"
              required
            />
          </div>
        </div>

        {/* Start and End Time */}
        <div className="grid grid-cols-2 gap-5">
          <div>
            <label className="block mb-1 font-semibold text-gold">
              Start Time
            </label>
            <input
              type="time"
              name="start_time"
              value={eventData.start_time}
              onChange={handleInputChange}
              className="w-full px-3 py-2 rounded border border-gold bg-black text-gold"
              required
            />
          </div>
          <div>
            <label className="block mb-1 font-semibold text-gold">
              End Time
            </label>
            <input
              type="time"
              name="end_time"
              value={eventData.end_time}
              onChange={handleInputChange}
              className="w-full px-3 py-2 rounded border border-gold bg-black text-gold"
              required
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="text-center font-semibold">
          <button
            type="submit"
            className="w-full px-4 py-2 bg-gold rounded mt-4"
          >
            {eventId ? "Update Event" : "Create Event"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default EventForm;
