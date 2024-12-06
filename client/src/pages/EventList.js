import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const EventList = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await axios.get("/events");
      setEvents(response.data);
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  };

  const handleEdit = (eventId) => {
    // Navigate to the edit page for the selected event
    window.location.href = `/edit/${eventId}`;
  };

  const handleDelete = async (eventId) => {
    try {
      await axios.delete(`/events/${eventId}`);
      setEvents((prevEvents) =>
        prevEvents.filter((event) => event.event_id !== eventId)
      );
    } catch (error) {
      console.error("Error deleting event:", error);
    }
  };

  return (
    <div className="container mx-auto p-5">
      <h1 className="text-center text-3xl font-bold mb-6">All Events</h1>
      <div className="flex justify-center">
        <Link to="/add-event" className="bg-gold text-black px-4 py-2 rounded">
          Add Event
        </Link>
        <Link
          to="/statistics"
          className="bg-gold text-black px-4 py-2 rounded ml-4"
        >
          Event Statistics
        </Link>
      </div>

      <div className="grid grid-cols-3 gap-4 mt-6">
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
            <div className="flex justify-center gap-2 mt-4">
              <button
                onClick={() => handleEdit(event.event_id)}
                className="bg-gold text-black px-4 py-2 rounded"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(event.event_id)}
                className="bg-red-500 text-white px-4 py-2 rounded"
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventList;
