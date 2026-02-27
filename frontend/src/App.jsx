import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Assessment from './pages/Assessment';
import Results from './pages/Results';

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/assess" element={<Assessment />} />
            <Route path="/results" element={<Results />} />
        </Routes>
    );
}

export default App;
