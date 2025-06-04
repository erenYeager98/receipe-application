
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { FaStar, FaRegStar } from 'react-icons/fa';

const API_URL = 'http://localhost:8000/api';

export default function App() {
  const [recipes, setRecipes] = useState([]);
  const [selected, setSelected] = useState(null);
  const [filters, setFilters] = useState({});
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(15);
  const [total, setTotal] = useState(0);

  const fetchData = async () => {
    const params = { ...filters, page, limit };
    const response = await axios.get(`${API_URL}/recipes`, { params });
    setRecipes(response.data.data);
    setTotal(response.data.total);
  };

  useEffect(() => {
    fetchData();
  }, [filters, page, limit]);

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => i < rating ? <FaStar key={i} color="gold" /> : <FaRegStar key={i} />);
  };

  return (
    <div style={{ display: 'flex', padding: 20 }}>
      <div style={{ flex: 2 }}>
        <h2>Recipes</h2>
        <div>
          <label>Title Filter: </label>
          <input onChange={e => setFilters({ ...filters, title: e.target.value })} />
        </div>
        <div>
          <button onClick={() => setFilters({})}>Clear Filters</button>
          </div>
          <div>
    <button onClick={async () => {
    try {
      const res = await axios.get(`${API_URL}/recipes/search`, {
        params: { title: filters.title }
      });
      if (res.data.data?.length > 0) {
        setSelected(res.data.data[0]);
      } else {
        alert('No recipe found with that title');
      }
    } catch (err) {
      console.error(err);
      alert('Error fetching recipe');
    }
  }}>Search</button>
          </div>
        <table border="1" width="100%">
          <thead>
            <tr>
              <th>Title</th>
              <th>Cuisine</th>
              <th>Rating</th>
              <th>Total Time</th>
              <th>Serves</th>
            </tr>
          </thead>
          <tbody>
            {recipes.length === 0 ? (
              <tr><td colSpan="5" align="center">No results found.</td></tr>
            ) : recipes.map(r => (
              <tr key={r.id} onClick={() => setSelected(r)}>
                <td>{r.title.length > 20 ? r.title.slice(0, 20) + '...' : r.title}</td>
                <td>{r.cuisine}</td>
                <td>{renderStars(Math.round(r.rating || 0))}</td>
                <td>{r.total_time}</td>
                <td>{r.serves}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <div style={{ marginTop: 10 }}>
          <label>Per Page: </label>
          <select onChange={e => setLimit(Number(e.target.value))} value={limit}>
            {[15, 20, 30, 50].map(n => <option key={n} value={n}>{n}</option>)}
          </select>

          <button disabled={page === 1} onClick={() => setPage(p => p - 1)}>Prev</button>
          <span style={{ margin: '0 10px' }}>Page {page}</span>
          <button disabled={page * limit >= total} onClick={() => setPage(p => p + 1)}>Next</button>
        </div>
      </div>

      {selected && (
        <div style={{ flex: 1, borderLeft: '1px solid #ccc', paddingLeft: 20 }}>
          <h3>{selected.title}</h3>
          <p><b>Cuisine:</b> {selected.cuisine}</p>
          <p><b>Description:</b> {selected.description}</p>
          <details>
            <summary><b>Total Time:</b> {selected.total_time} mins</summary>
            <p>Prep: {selected.prep_time} mins, Cook: {selected.cook_time} mins</p>
          </details>

          <h4>Nutrients</h4>
          <table>
            <tbody>
              {selected.nutrients && Object.entries(selected.nutrients).map(([key, value]) => (
                <tr key={key}>
                  <td><b>{key}</b></td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
