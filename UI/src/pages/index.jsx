import { useState, useEffect } from "react";
import axios from "axios";
import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";
import Modal from "react-modal";

Modal.setAppElement("#__next");

const JobMapPage = () => {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);

  useEffect(() => {
    // Fetch job data from your API here and set it in the state
    axios
      .get("/api/jobs")
      .then((response) => setJobs(response.data))
      .catch((error) => console.error(error));
  }, []);

  const handleJobClick = (job) => {
    setSelectedJob(job);
  };

  return (
    <div>
      <LoadScript googleMapsApiKey="YOUR_API_KEY">
        <GoogleMap
          center={{ lat: 0, lng: 0 }} // Set initial map center coordinates
          zoom={4} // Set initial zoom level
        >
          {jobs.map((job, index) => (
            <Marker
              key={index}
              position={{ lat: job.LATITUDE, lng: job.LONGITUDE }} // Replace with your data
              onClick={() => handleJobClick(job)}
            />
          ))}
        </GoogleMap>
      </LoadScript>

      {selectedJob && (
        <Modal isOpen={true} onRequestClose={() => setSelectedJob(null)}>
          <h2>{selectedJob.JobTitle}</h2>
          <p>Company: {selectedJob.Company}</p>
          <p>Region: {selectedJob.Region}</p>
          <p>Mode: {selectedJob.Mode}</p>
          <p>Publish Duration: {selectedJob.PublishDuration}</p>
          <button onClick={() => (window.location.href = selectedJob.Link)}>
            Show More
          </button>
        </Modal>
      )}
    </div>
  );
};

export default JobMapPage;
