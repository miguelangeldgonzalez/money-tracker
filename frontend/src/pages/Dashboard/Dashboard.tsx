import React from "react";
import RegisterLastTransaction from "../../components/RegisterLastTransaction/RegisterLastTransaction";
import "./Dashboard.css";

const Dashboard: React.FC = () => {
  return (
    <div className="dashboard-grid">
      <RegisterLastTransaction />
      {/* Add more dashboard widgets/components here */}
    </div>
  );
};

export default Dashboard;
