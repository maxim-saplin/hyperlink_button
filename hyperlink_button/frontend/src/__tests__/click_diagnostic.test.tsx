/**
 * Diagnostic tests for HyperlinkButton click reliability.
 *
 * These tests verify the click-handling path under:
 *   1. Normal rendering (no StrictMode)
 *   2. React 18 StrictMode (double-invokes state updaters in dev)
 *
 * Hypothesis: Streamlit.setComponentValue() is called INSIDE a React
 * state updater function (setClickCount).  Under StrictMode, updater
 * functions are invoked twice, causing the side-effect to fire twice
 * per single user click.
 */

import React from "react"
import ReactDOM from "react-dom/client"
import { describe, test, expect, vi, beforeEach, afterEach } from "vitest"
import { render, fireEvent, act, cleanup } from "@testing-library/react"

// ── Mock streamlit-component-lib before importing the component ──

const setComponentValueCalls: any[] = []

vi.mock("streamlit-component-lib", () => {
  return {
    Streamlit: {
      setComponentValue: (val: any) => {
        setComponentValueCalls.push(val)
      },
      setFrameHeight: vi.fn(),
      setComponentReady: vi.fn(),
      RENDER_EVENT: "streamlit:render",
      events: new EventTarget(),
    },
    StreamlitComponentBase: class {
      props: any
      state: any
    },
    withStreamlitConnection: (Component: React.ComponentType<any>) => {
      // Simplified: just pass through, injecting minimal props
      return (outerProps: any) => {
        const defaultArgs = {
          label: "Test Link",
          disabled: false,
          type: "secondary",
          icon_position: "left",
          width: "content",
          ...outerProps,
        }
        return <Component args={defaultArgs} width={300} disabled={false} />
      }
    },
  }
})

// Import AFTER mocking
import HyperlinkButton from "../HyperlinkButton"

// ── Helpers ──

function clearCalls() {
  setComponentValueCalls.length = 0
}

// ── Tests ──

describe("Click diagnostic – setComponentValue side-effect placement", () => {
  beforeEach(() => {
    clearCalls()
  })

  afterEach(() => {
    cleanup()
  })

  test("DIAGNOSTIC: single click WITHOUT StrictMode fires setComponentValue exactly once", () => {
    // Render WITHOUT StrictMode
    const { container } = render(<HyperlinkButton />)
    const button = container.querySelector("button.hb-button")!
    expect(button).toBeTruthy()

    clearCalls()
    fireEvent.click(button)

    // Without StrictMode, the state updater runs once → one side effect
    expect(setComponentValueCalls).toEqual([1])
  })

  test("single click WITH StrictMode still fires once", () => {
    // Render WITH StrictMode; side effects should still run once.
    const { container } = render(
      <React.StrictMode>
        <HyperlinkButton />
      </React.StrictMode>
    )
    const button = container.querySelector("button.hb-button")!
    expect(button).toBeTruthy()

    clearCalls()
    fireEvent.click(button)

    expect(setComponentValueCalls).toEqual([1])
  })

  test("DIAGNOSTIC: rapid consecutive clicks each register incrementing values", () => {
    const { container } = render(<HyperlinkButton />)
    const button = container.querySelector("button.hb-button")!

    clearCalls()

    // 5 rapid clicks
    for (let i = 0; i < 5; i++) {
      fireEvent.click(button)
    }

    console.log(
      "setComponentValue calls after 5 rapid clicks:",
      JSON.stringify(setComponentValueCalls)
    )

    // Each click should produce a strictly increasing value
    // Filter to unique sequential values
    const uniqueValues = setComponentValueCalls.filter(
      (v, i, arr) => i === 0 || v !== arr[i - 1]
    )
    expect(uniqueValues).toEqual([1, 2, 3, 4, 5])
  })

  test("Enter keydown alone does not fire activation", () => {
    const { container } = render(<HyperlinkButton />)
    const button = container.querySelector("button.hb-button")!

    clearCalls()

    // Native button keyboard behavior triggers click events; keydown alone should not.
    fireEvent.keyDown(button, { key: "Enter" })

    expect(setComponentValueCalls).toEqual([])
  })

  test("Enter key + synthesized click results in a single activation", () => {
    const { container } = render(<HyperlinkButton />)
    const button = container.querySelector("button.hb-button")!

    clearCalls()

    // Simulate what a real browser does: keydown → click (synthesized by browser)
    fireEvent.keyDown(button, { key: "Enter" })
    fireEvent.click(button)

    expect(setComponentValueCalls).toEqual([1])
  })

  test("Space key + synthesized click results in a single activation", () => {
    const { container } = render(<HyperlinkButton />)
    const button = container.querySelector("button.hb-button")!

    clearCalls()

    // Space on a button: keydown -> keyup -> click.
    fireEvent.keyDown(button, { key: " " })
    fireEvent.click(button)

    expect(setComponentValueCalls).toEqual([1])
  })
})

describe("Click diagnostic – counter seeding after remount", () => {
  /**
   * This test suite verifies what happens when the React component is
   * unmounted and remounted (simulating iframe recreation) while the
   * Python-side last_seen counter persists.
   */

  beforeEach(() => {
    clearCalls()
  })

  afterEach(() => {
    cleanup()
  })

  test("remount uses last_click_count seed to continue counter", () => {
    // First mount: click twice
    const result1 = render(<HyperlinkButton />)
    const button1 = result1.container.querySelector("button.hb-button")!

    fireEvent.click(button1)
    fireEvent.click(button1)

    const valuesBeforeUnmount = [...setComponentValueCalls]
    expect(valuesBeforeUnmount).toEqual([1, 2])

    // Unmount and remount (simulates iframe recreation)
    result1.unmount()
    clearCalls()

    const result2 = render(<HyperlinkButton last_click_count={2} />)
    const button2 = result2.container.querySelector("button.hb-button")!

    // Click once on the remounted component
    fireEvent.click(button2)

    // First click after remount should continue from last_seen(2) to 3.
    expect(setComponentValueCalls).toEqual([3])

    // Document the mismatch
    const pythonLastSeen = valuesBeforeUnmount[valuesBeforeUnmount.length - 1]
    const reactNewValue = setComponentValueCalls[0]
    const wouldBeDetected = reactNewValue > pythonLastSeen

    expect(wouldBeDetected).toBe(true)
  })
})
