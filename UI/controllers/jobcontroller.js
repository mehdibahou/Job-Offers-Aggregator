// pages/api/cassandraData.js
import { Client } from "cassandra-driver";
import { StatusCodes } from "http-status-codes";

const cassandra = new Client({
  contactPoints: ["YOUR_CASSANDRA_HOST"],
  localDataCenter: "datacenter1",
  keyspace: "your_keyspace",
});

cassandra
  .connect()
  .then(() => {
    console.log("Connected to Cassandra");
  })
  .catch((err) => {
    console.error("Error connecting to Cassandra", err);
  });

const getjobs = async (req, res) => {
  try {
    const query = "SELECT * FROM your_table"; // Replace with your query
    const result = await cassandra.execute(query);

    // Process the Cassandra query result as needed
    const data = result.rows;

    res.status(StatusCodes.OK).json({ data });
  } catch (error) {
    console.error("Cassandra query error:", error);
    res
      .status(StatusCodes.INTERNAL_SERVER_ERROR)
      .json({ error: "Internal Server Error" });
  }
};
module.exports = {
  getjobs,
};
