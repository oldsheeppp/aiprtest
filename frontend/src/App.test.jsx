import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";

import App from "./App.jsx";


const jsonResponse = (body, status = 200) =>
  Promise.resolve({
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(body)
  });


describe("App", () => {
  beforeEach(() => {
    global.fetch = vi.fn((url, options = {}) => {
      if (url === "/users/1") {
        return jsonResponse({ id: 1, email: "ada@example.com", name: "Ada Lovelace" });
      }
      if (url === "/users/999") {
        return jsonResponse({ detail: "user not found" }, 404);
      }
      if (url === "/payments/charge") {
        const body = JSON.parse(options.body);
        return jsonResponse({
          id: "pay_1",
          user_id: body.user_id,
          amount_cents: body.amount_cents,
          currency: body.currency,
          status: "charged"
        });
      }
      if (url === "/payments/refund") {
        return jsonResponse({
          id: "pay_1",
          user_id: 1,
          amount_cents: 2500,
          currency: "USD",
          status: "refunded"
        });
      }
      if (url === "/admin/audit-log") {
        return jsonResponse({ events: [{ event: "sandbox_started" }] });
      }
      throw new Error(`Unhandled request: ${url}`);
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  test("loads the default user profile", async () => {
    render(<App />);

    expect(await screen.findByText("Ada Lovelace")).toBeInTheDocument();
    expect(screen.getByText("ada@example.com")).toBeInTheDocument();
  });

  test("shows a clear message when a user is missing", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.clear(screen.getByLabelText("User ID"));
    await user.type(screen.getByLabelText("User ID"), "999");
    await user.click(screen.getByRole("button", { name: /load user/i }));

    expect(await screen.findByText("user not found")).toBeInTheDocument();
  });

  test("charges and refunds a payment", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.clear(screen.getByLabelText("Amount in cents"));
    await user.type(screen.getByLabelText("Amount in cents"), "2500");
    await user.click(screen.getByRole("button", { name: /charge/i }));
    expect(await screen.findByText("pay_1 charged")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /refund/i }));
    expect(await screen.findByText("pay_1 refunded")).toBeInTheDocument();
  });

  test("loads audit events with the admin role header", async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.click(screen.getByRole("button", { name: /load audit log/i }));

    expect(await screen.findByText("sandbox_started")).toBeInTheDocument();
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        "/admin/audit-log",
        expect.objectContaining({
          headers: { "X-Role": "admin" }
        })
      );
    });
  });
});
