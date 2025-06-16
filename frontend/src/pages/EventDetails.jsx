import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Calendar, MapPin, Users, Clock, Star, ArrowLeft, Share2, Heart, Loader, AlertCircle } from 'lucide-react';
import { eventsAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const EventDetails = () => {
  const { id } = useParams();
  const { isAuthenticated } = useAuth();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [registering, setRegistering] = useState(false);
  const [registered, setRegistered] = useState(false);

  useEffect(() => {
    fetchEvent();
  }, [id]);

  const fetchEvent = async () => {
    try {
      setLoading(true);
      const data = await eventsAPI.getEventById(id);
      setEvent(data.event || data);
    } catch (err) {
      setError('Failed to load event details');
      console.error('Error fetching event:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async () => {
    if (!isAuthenticated) {
      alert('Please login to register for events');
      return;
    }

    try {
      setRegistering(true);
      await eventsAPI.registerForEvent(id);
      setRegistered(true);
      alert('Successfully registered for the event!');
    } catch (err) {
      alert('Failed to register for event. Please try again.');
      console.error('Registration error:', err);
    } finally {
      setRegistering(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="h-8 w-8 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Loading event details...</p>
        </div>
      </div>
    );
  }

  if (error || !event) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Event Not Found</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link 
            to="/events"
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Back to Events
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Back Button */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link 
            to="/events" 
            className="inline-flex items-center text-blue-600 hover:text-blue-800 transition-colors duration-200"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Events
          </Link>
        </div>
      </div>

      {/* Hero Image */}
      <div className="relative h-96 overflow-hidden">
        <img 
          src={event.image || 'https://images.pexels.com/photos/2833037/pexels-photo-2833037.jpeg?auto=compress&cs=tinysrgb&w=800'} 
          alt={event.title}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black bg-opacity-40"></div>
        <div className="absolute bottom-6 left-6 text-white">
          <span className="bg-blue-600 px-3 py-1 rounded-full text-sm font-medium">
            {event.category || 'Event'}
          </span>
        </div>
        <div className="absolute top-6 right-6 flex space-x-2">
          <button className="bg-white bg-opacity-20 backdrop-blur-sm text-white p-2 rounded-full hover:bg-opacity-30 transition-all duration-200">
            <Share2 className="h-5 w-5" />
          </button>
          <button className="bg-white bg-opacity-20 backdrop-blur-sm text-white p-2 rounded-full hover:bg-opacity-30 transition-all duration-200">
            <Heart className="h-5 w-5" />
          </button>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Event Header */}
            <div>
              <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
                {event.title}
              </h1>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-gray-600">
                <div className="flex items-center">
                  <Calendar className="h-5 w-5 mr-3 text-blue-500" />
                  <span>{formatDate(event.date)}</span>
                </div>
                <div className="flex items-center">
                  <Clock className="h-5 w-5 mr-3 text-blue-500" />
                  <span>{event.time}</span>
                </div>
                <div className="flex items-center">
                  <MapPin className="h-5 w-5 mr-3 text-blue-500" />
                  <span>{event.location}</span>
                </div>
                <div className="flex items-center">
                  <Users className="h-5 w-5 mr-3 text-blue-500" />
                  <span>{event.maxAttendees || event.attendees || 0} attendees expected</span>
                </div>
              </div>
            </div>

            {/* Description */}
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-4">About This Event</h2>
              <p className="text-gray-600 leading-relaxed whitespace-pre-line">
                {event.description}
              </p>
            </div>

            {/* Additional Details */}
            {event.agenda && (
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Event Agenda</h2>
                <div className="space-y-4">
                  {event.agenda.map((item, index) => (
                    <div key={index} className="flex items-start space-x-4 p-4 bg-white rounded-lg shadow-sm border border-gray-100">
                      <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium whitespace-nowrap">
                        {item.time}
                      </div>
                      <div className="text-gray-700 font-medium">
                        {item.activity}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Booking Card */}
            <div className="bg-white rounded-xl shadow-lg p-6 sticky top-6">
              <div className="text-center mb-6">
                <div className="text-3xl font-bold text-gray-900 mb-2">
                  ${event.price || 'Free'}
                </div>
                <p className="text-gray-600">per person</p>
              </div>

              <button 
                onClick={handleRegister}
                disabled={registering || registered}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl mb-4 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
              >
                {registering ? 'Registering...' : registered ? 'Registered!' : 'Register Now'}
              </button>

              <div className="text-center text-sm text-gray-600 mb-6">
                Free cancellation up to 48 hours before the event
              </div>

              <div className="border-t pt-6">
                <h3 className="font-semibold text-gray-900 mb-3">Event Organizer</h3>
                <div className="flex items-center space-x-3 mb-3">
                  <div className="bg-gradient-to-r from-blue-600 to-purple-600 w-10 h-10 rounded-full flex items-center justify-center">
                    <span className="text-white font-bold">
                      {event.organizer?.name?.charAt(0) || 'EP'}
                    </span>
                  </div>
                  <div>
                    <p className="font-medium text-gray-900">
                      {event.organizer?.name || 'EventPro'}
                    </p>
                    <div className="flex items-center text-sm text-gray-600">
                      <Star className="h-4 w-4 text-yellow-400 mr-1" />
                      <span>4.9 • 150+ events</span>
                    </div>
                  </div>
                </div>
                <p className="text-sm text-gray-600">
                  {event.organizer?.description || 'Professional event management company specializing in creating memorable experiences.'}
                </p>
              </div>
            </div>

            {/* Location Map Placeholder */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Event Location</h3>
              <div className="bg-gray-200 rounded-lg h-48 flex items-center justify-center mb-4">
                <MapPin className="h-12 w-12 text-gray-400" />
              </div>
              <p className="text-gray-700 font-medium mb-2">{event.venue || 'Event Venue'}</p>
              <p className="text-gray-600 text-sm">
                {event.location}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventDetails;