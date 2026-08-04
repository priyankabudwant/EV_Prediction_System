import { render, screen } from '@testing-library/react';
import App from './App';

test('renders loading dashboard text', () => {
  render(<App />);
  const textElement = screen.getByText(/loading dashboard/i);
  expect(textElement).toBeInTheDocument();
});
