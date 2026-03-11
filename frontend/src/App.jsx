import './App.css'
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import DistanceCalculator from './components/DistanceCalculator'
import HistoricalQueries from './components/HistoricalQueries'

function App() {
  return (
    <Router>
      <div className="app-container">
        <Routes>
          <Route path="/" element={<DistanceCalculator />} />
          <Route path="/history" element={<HistoricalQueries />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
