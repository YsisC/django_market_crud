import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { MarketsPage } from './pages/MarketsPage';
import { Toaster } from "react-hot-toast";

function App() {

  return (
    <BrowserRouter>
    <div className="container mx-auto">
    
      <Routes>
        <Route path="/" element={<Navigate to="/markets" />} />
        <Route path="/markets" element={<MarketsPage />} />
  
      </Routes>
      <Toaster />
    </div>
  </BrowserRouter>
  )
}

export default App
