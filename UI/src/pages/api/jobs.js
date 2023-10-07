import nc from "next-connect";
import { getjobs } from "../../../controllers/jobcontroller";
const router = nc({
  onError: (err, req, res) => {
    console.error(err.stack);
    res.status(500).end("Something broke!");
  },
  onNoMatch: (req, res) => {
    res.status(404).end("Page is not found");
  },
});

router.get(getjobs);

export default router;
