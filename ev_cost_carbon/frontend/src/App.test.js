import { fireEvent, render, screen } from "@testing-library/react";
import App from "./App";

test("renders the GreenVolt predictor heading", () => {
  render(<App />);
  expect(screen.getByText(/greenvolt ev cost and carbon predictor/i)).toBeInTheDocument();
});

test("allows switching to the research model", () => {
  render(<App />);
  fireEvent.click(screen.getByRole("button", { name: /research model/i }));
  expect(screen.getAllByText(/selected: research model/i)[0]).toBeInTheDocument();
});
