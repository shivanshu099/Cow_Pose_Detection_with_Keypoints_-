import React, { useState } from 'react';
import './classification.css';
import api from '../api';

const Classification = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [predictImg, setPredictImg] = useState(null);
  const [file, setFile] = useState(null);

  // handle file change
  const handleChange = (e) => {
    setFile(e.target.files[0]);
  };

  // handle form submit
  const handleSubmit = async (e) => {
    e.preventDefault(); // prevent page reload
    setLoading(true);
    setError(null);
    setData(null);

    if (!file) {
      setError("Please upload an image");
      setLoading(false);
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await api.post("/predict", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setData({
        metrics: res.data.metrics,
        scores: res.data.scores,
      });
      setPredictImg(res.data.predict_img);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="classification-container">
      
      <div className="instructions">
        <p>
          <strong>Example of an image you should upload:</strong>
        </p>
        <img
          src="https://tse4.mm.bing.net/th/id/OIP.IvoZWTzwI7TLNx5OjXqVcAHaGj?rs=1&pid=ImgDetMain&o=7&rm=3"
          alt="Example cattle for classification"
          className="example-image"
        />
      </div>

      <form onSubmit={handleSubmit}>
        <h2>Cattle Classification</h2>
        <input type="file" name="image_cattle" onChange={handleChange} />
        <button type="submit">
          {loading ? "Loading..." : "Predict"}
        </button>
      </form>

      {error && <p className='error'>Error: {error}</p>}

      {data && (
        <div className="result">
          <h3>Metrics & Scores</h3>
          <pre>{JSON.stringify(data.metrics, null, 2)}</pre>
          <pre>{JSON.stringify(data.scores, null, 2)}</pre>
        </div>
      )}

      {predictImg && (
        <div className='image-preview'>
          <h3>Result Image</h3>
          <img
            src={`data:image/jpeg;base64,${predictImg}`}
            alt="Prediction"
          />
        </div>
      )}
    </div>
  )
}

export default Classification
