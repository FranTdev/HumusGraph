import { useState } from 'react'
import './App.css' // We might remove this if we rely solely on index.css or clean it up
import Dashboard from './components/Dashboard'

function App() {
  return (
    <>
      <h1>Monitor de Vermicompost</h1>
      <Dashboard />
    </>
  )
}

export default App
