import React, { useState, useEffect } from 'react';
import { Loader, Upload, Calendar, Clock, MapPin, Ticket, Users, Save } from 'lucide-react';
import { useNavigate, useParams } from 'react-router-dom';
import { eventsAPI } from '../services/api';

const CLOUDINARY_URL = 'https://api.cloudinary.com/v1_1/ddltxgibq/image/upload';
const CLOUDINARY_PRESET = 'event_upload_preset';

const UpdateEvent = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    date: '',
    time: '',
    location: '',
    venue: '',
    category: 'Conference',
    price: 0,
    maxAttendees: 100,
    status: 'draft',
    image: ''
  });

  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    const fetchEvent = async () => {
      try {
        setLoading(true);
        const response = await eventsAPI.getEventById(id); // ✅ Correct API
  
        if (!response || !response.event) {
          throw new Error('Event not found');
        }
  
        const eventDate = new Date(response.event.date);
        const formattedDate = eventDate.toISOString().split('T')[0];
  
        setFormData({
          ...response.event,
          date: formattedDate,
        });
      } catch (err) {
        console.error('Error fetching event:', err);
        setError(err.message || 'Failed to fetch event data');
      } finally {
        setLoading(false);
      }
    };
  
    fetchEvent();
  }, [id]);

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const data = new FormData();
    data.append('file', file);
    data.append('upload_preset', CLOUDINARY_PRESET);

    try {
      const response = await fetch(CLOUDINARY_URL, {
        method: 'POST',
        body: data
      });
      const result = await response.json();
      setFormData(prev => ({ ...prev, image: result.secure_url }));
    } catch (err) {
      console.error('Cloudinary upload failed:', err);
      setError('Image upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);
      await eventsAPI.updateEvent(id, formData);
      setSuccessMsg('Event updated successfully!');
      setTimeout(() => navigate('/events'), 1500);
    } catch (err) {
      console.error('Error updating event:', err);
      setError(err.message || 'Failed to update event');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <Loader className="animate-spin text-blue-500 h-12 w-12" />
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto p-8 bg-white rounded-xl shadow-lg mt-10 mb-20 border border-gray-100">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-blue-600 mb-2">Update Event</h2>
        <p className="text-gray-600">Edit the event details below</p>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 rounded-lg border border-red-200">
          <p className="text-red-500 font-medium">{error}</p>
        </div>
      )}
      
      {successMsg && (
        <div className="mb-6 p-4 bg-green-50 rounded-lg border border-green-200">
          <p className="text-green-600 font-medium">{successMsg}</p>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Title */}
          <div className="col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Event Title</label>
            <div className="relative">
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="Enter event title"
                className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Ticket className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          {/* Description */}
          <div className="col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter event description"
              rows="4"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>

          {/* Date and Time */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <div className="relative">
              <input
                type="date"
                name="date"
                value={formData.date}
                onChange={handleChange}
                className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Calendar className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Time</label>
            <div className="relative">
              <input
                type="time"
                name="time"
                value={formData.time}
                onChange={handleChange}
                className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Clock className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          {/* Location and Venue */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
            <div className="relative">
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="City, Country"
                className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                required
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MapPin className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Venue</label>
            <input
              type="text"
              name="venue"
              value={formData.venue}
              onChange={handleChange}
              placeholder="Venue name"
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>

          {/* Category and Status */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="Conference">Conference</option>
              <option value="Workshop">Workshop</option>
              <option value="Seminar">Seminar</option>
              <option value="Social">Social</option>
              <option value="Concert">Concert</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="draft">Draft</option>
              <option value="published">Published</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          {/* Price and Max Attendees */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Price ($)</label>
            <div className="relative">
              <input
                type="number"
                name="price"
                value={formData.price}
                onChange={handleChange}
                placeholder="0"
                min="0"
                className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <span className="text-gray-400">$</span>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Max Attendees</label>
            <div className="relative">
              <input
                type="number"
                name="maxAttendees"
                value={formData.maxAttendees}
                onChange={handleChange}
                placeholder="100"
                min="1"
                className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Users className="h-5 w-5 text-gray-400" />
              </div>
            </div>
          </div>
        </div>

        {/* Image Upload */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Event Image</label>
          {formData.image && (
            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-2">Current Image:</p>
              <img 
                src={formData.image} 
                alt="Current event" 
                className="h-48 w-full rounded-lg object-cover border border-gray-200"
              />
            </div>
          )}
          <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-xl">
            <div className="space-y-1 text-center">
              <div className="flex text-sm text-gray-600 justify-center">
                <label
                  htmlFor="file-upload"
                  className="relative cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none"
                >
                  <span>Upload a new image</span>
                  <input
                    id="file-upload"
                    name="file-upload"
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="sr-only"
                  />
                </label>
                <p className="pl-1">or drag and drop</p>
              </div>
              <p className="text-xs text-gray-500">PNG, JPG, GIF up to 10MB</p>
            </div>
          </div>
          {uploading && (
            <div className="mt-4 flex items-center justify-center">
              <Loader className="animate-spin text-blue-500 h-6 w-6 mr-2" />
              <span className="text-gray-600">Uploading...</span>
            </div>
          )}
        </div>

        {/* Submit Button */}
        <div className="pt-4 flex gap-4">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="w-1/3 bg-gray-200 text-gray-800 py-3 rounded-lg hover:bg-gray-300 transition duration-200 flex items-center justify-center shadow-md hover:shadow-lg"
          >
            <span className="font-medium">Cancel</span>
          </button>
          <button
            type="submit"
            disabled={loading}
            className="w-2/3 bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg hover:from-blue-700 hover:to-purple-700 transition duration-200 flex items-center justify-center shadow-md hover:shadow-lg disabled:opacity-70"
          >
            {loading ? (
              <Loader className="animate-spin h-5 w-5 mr-2" />
            ) : (
              <Save className="h-5 w-5 mr-2" />
            )}
            <span className="font-medium">{loading ? 'Updating...' : 'Save Changes'}</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default UpdateEvent;