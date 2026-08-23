import express from "express";
import bodyparser from "body-parser";
import connectDb from "./src/utils/db.js";
import routes from "./src/routes/routes.js";
import cors from "cors";
import swaggerUi from "swagger-ui-express";
import swaggerJsdoc from "swagger-jsdoc";
import swaggerOptions from "./src/swagger/swaggerOptions.js";

const PORT = 3000;
const app = express();
const swaggerSpec = swaggerJsdoc(swaggerOptions);

app.use(cors());
app.use(bodyparser.urlencoded({ extended: false }));
app.use(bodyparser.json());

app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader(
    "Access-Control-Allow-Headers",
    "Origin , X-Requested-With , Content-Type , Accept , Authorization"
  );
  res.setHeader(
    "Access-Control-Allow-Methods",
    "GET , POST , PATCH , DELETE , OPTIONS"
  );
  next();
});

app.use("/api/docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));

app.get("/api/healthCheck", (req, res) => {
  res.json({ Status: "OK" });
});

app.use(routes);

app.listen(PORT, () => console.log(`Server Started on port ${PORT}`));
connectDb();
