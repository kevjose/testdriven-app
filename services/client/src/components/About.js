import './AutoSuggest.css';
import React from 'react';
import Autosuggest from 'react-autosuggest';
import DayPicker, { DateUtils } from 'react-day-picker';
import 'react-day-picker/lib/style.css';
import _ from 'lodash';
import axios from 'axios';

class About extends React.Component {
  constructor() {
    super();

    this.state = {
      value: '',
      suggestions: [],
      isLoading: false,
      selectedDays: []
    };
    this.handleDayClick = this.handleDayClick.bind(this);
    this.debouncedLoadSuggestions = _.debounce(this.loadSuggestions, 300); // 1000ms is chosen for demo purposes only.
  }

  getSuggestionValue = suggestion => suggestion.name;
  renderSuggestion = suggestion => (
    <span>
      {suggestion.name} ({suggestion.business_unit}|
      {suggestion.reporting_manager})
    </span>
  );

  handleDayClick(day, { selected }) {
    const { selectedDays } = this.state;
    if (selected) {
      const selectedIndex = selectedDays.findIndex(selectedDay =>
        DateUtils.isSameDay(selectedDay, day)
      );
      selectedDays.splice(selectedIndex, 1);
    } else {
      selectedDays.push(day);
    }
    this.setState({ selectedDays });
  }

  loadSuggestions(value) {
    this.setState({
      isLoading: true
    });
    const options = {
      url: `${
        process.env.REACT_APP_USERS_SERVICE_URL
      }/leave_tracker/employee/autofill/${value}`,
      method: 'get',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${window.localStorage.authToken}`
      }
    };
    return axios(options)
      .then(res => {
        this.setState({
          isLoading: false,
          suggestions: res.data.data.employees
        });
      })
      .catch(error => {
        console.log(error);
        this.setState({
          isLoading: false
        });
      });
  }

  onChange = (event, { newValue }) => {
    this.setState({
      value: newValue
    });
  };

  onSuggestionsFetchRequested = ({ value }) => {
    this.debouncedLoadSuggestions(value);
  };

  onSuggestionsClearRequested = () => {
    this.setState({
      suggestions: []
    });
  };

  render() {
    const { value, suggestions, isLoading } = this.state;
    const inputProps = {
      placeholder: 'Start Typing Employee Name',
      value,
      onChange: this.onChange
    };
    const status = isLoading ? 'Loading...' : 'Type to load suggestions';

    return (
      <div>
        <div>
          <strong>Employee Name:</strong>{' '}
          <small>
            <em>{status}</em>
          </small>
        </div>
        <Autosuggest
          suggestions={suggestions}
          onSuggestionsFetchRequested={this.onSuggestionsFetchRequested}
          onSuggestionsClearRequested={this.onSuggestionsClearRequested}
          getSuggestionValue={this.getSuggestionValue}
          renderSuggestion={this.renderSuggestion}
          inputProps={inputProps}
        />

        <br />
        <div>
          <strong>Select days for which leave has been aaplied:</strong>
        </div>
        <DayPicker
          selectedDays={this.state.selectedDays}
          onDayClick={this.handleDayClick}
          disabledDays={[{ daysOfWeek: [0, 6] }]}
        />
        <pre>{this.state.value}</pre>
        <br />
        <div>
          <button className="button is-primary is-fullwidth">Sumbit</button>
        </div>
      </div>
    );
  }
}

export default About;
