import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import EventStatistics from "./pages/EventStatistics";
import EventList from "./pages/EventList";
import EventForm from "./pages/EventForm";

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<EventList />} />
          <Route path="/create" element={<EventForm />} />
          <Route path="/edit/:eventId" element={<EventForm />} />
          <Route path="/statistics" element={<EventStatistics />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
