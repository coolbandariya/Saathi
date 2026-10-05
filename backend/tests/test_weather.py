from app.weather import OpenMeteoWeather

def test_weather_rejects_invalid_coordinates():
    result=OpenMeteoWeather().forecast(95,77)
    assert result.ok is False
    assert "Invalid coordinates" in result.message
