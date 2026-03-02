import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Chatbot from '../index'; // Adjust path as needed

// Mock the fetch API
global.fetch = jest.fn((url, options) => {
  if (url === 'http://localhost:8000/query' && options.method === 'POST') {
    const body = JSON.parse(options.body);
    if (body.question.includes('test question')) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({
          answer: 'This is a test answer for: ' + body.question,
          sources: [{ path: 'test_source.md', heading: 'Test Section', page: 1 }]
        }),
      });
    } else if (body.question.includes('error')) {
      return Promise.resolve({
        ok: false,
        status: 500,
      });
    }
  }
  return Promise.reject(new Error('unhandled fetch'));
});

describe('Chatbot', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders the floating button', () => {
    render(<Chatbot />);
    expect(screen.getByRole('button', { name: '?' })).toBeInTheDocument();
  });

  test('opens and closes the chat window', () => {
    render(<Chatbot />);
    const floatingButton = screen.getByRole('button', { name: '?' });
    fireEvent.click(floatingButton);
    expect(screen.getByText('Ask the Book')).toBeInTheDocument();

    const closeButton = screen.getByRole('button', { name: '×' });
    fireEvent.click(closeButton);
    expect(screen.queryByText('Ask the Book')).not.toBeInTheDocument();
  });

  test('sends a query and displays the response', async () => {
    render(<Chatbot />);
    fireEvent.click(screen.getByRole('button', { name: '?' }));

    const input = screen.getByPlaceholderText('Ask a question...');
    fireEvent.change(input, { target: { value: 'This is a test question' } });
    fireEvent.click(screen.getByRole('button', { name: 'Send' }));

    expect(screen.getByText('Loading...')).toBeInTheDocument();
    await screen.findByText('This is a test answer for: This is a test question');
    expect(screen.getByText('Sources:')).toBeInTheDocument();
    expect(screen.getByText('test_source.md')).toBeInTheDocument();
  });

  test('displays an error message if the API call fails', async () => {
    render(<Chatbot />);
    fireEvent.click(screen.getByRole('button', { name: '?' }));

    const input = screen.getByPlaceholderText('Ask a question...');
    fireEvent.change(input, { target: { value: 'This will cause an error' } });
    fireEvent.click(screen.getByRole('button', { name: 'Send' }));

    expect(screen.getByText('Loading...')).toBeInTheDocument();
    await screen.findByText('Sorry, something went wrong.');
  });
});
