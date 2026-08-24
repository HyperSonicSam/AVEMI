import json
import sys
import time
from copy import deepcopy
from pathlib import Path


# ---------------------------------------------------------
# Make project imports available
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ---------------------------------------------------------
# AVEMI imports
# ---------------------------------------------------------

from src.emotion.emotion_manager import (
    get_emotion_context,
    get_emotion_profile
)

from src.intents.intent_router import detect_intent

from src.vehicle.action_manager import (
    execute_action,
    execute_structured_action
)

from src.llm.command_parser import parse_command

from src.llm.prompt_builder import build_system_prompt

from src.llm.ollama_client import generate_response


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

TEST_CASES_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "test_cases.json"
)

RESULTS_FILE = (
    PROJECT_ROOT
    / "evaluation"
    / "evaluation_results.json"
)


# ---------------------------------------------------------
# Default vehicle state
# ---------------------------------------------------------

DEFAULT_VEHICLE_STATE = {
    "temperature": 22,
    "music_status": "Paused",
    "music_category": "None",
    "destination": "None",
    "navigation_active": False,
    "fuel_level": 62
}


# ---------------------------------------------------------
# Run one AVEMI interaction
# ---------------------------------------------------------

def run_case(
    test_case,
    assistant_mode
):
    vehicle_state = deepcopy(
        DEFAULT_VEHICLE_STATE
    )

    messages = []

    emotion = test_case.get(
        "emotion",
        "neutral"
    )

    # Controlled evaluation uses a fixed high-confidence
    # emotional context. This tests AVEMI's behaviour when
    # the emotional state is already known.
    emotion_confidence = 90

    emotion_context = get_emotion_context(
        assistant_mode,
        emotion.capitalize(),
        emotion_confidence
    )

    emotion_profile = get_emotion_profile(
        emotion_context
    )

    user_message = test_case["message"]

    start_time = time.perf_counter()

    # -----------------------------------------------------
    # Parse structured command
    # -----------------------------------------------------

    command = parse_command(
        user_message,
        vehicle_state,
        messages
    )

    # -----------------------------------------------------
    # Execute action
    # -----------------------------------------------------

    if command:
        action_response = (
            execute_structured_action(
                command,
                vehicle_state,
                emotion_profile
            )
        )

    else:
        intent = detect_intent(
            user_message
        )

        action_response = execute_action(
            intent,
            user_message,
            vehicle_state,
            emotion_profile
        )

    # -----------------------------------------------------
    # Determine predicted intent
    # -----------------------------------------------------

    intent = (
        command.get("intent")
        if command
        else "unknown"
    )

    # -----------------------------------------------------
    # Generate response
    # -----------------------------------------------------

    # Vehicle commands remain deterministic.
    if intent not in [
        "conversation",
        "unknown"
    ]:
        assistant_response = (
            action_response
        )

    else:
        system_prompt = (
            build_system_prompt(
                emotion_context,
                emotion_profile,
                vehicle_state
            )
        )

        llm_messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        assistant_response = (
            generate_response(
                llm_messages
            )
        )

    elapsed_time = (
        time.perf_counter()
        - start_time
    )

    return {
        "mode": assistant_mode,
        "predicted_intent": intent,
        "command": command,
        "response": assistant_response,
        "response_time_seconds": round(
            elapsed_time,
            3
        ),
        "vehicle_state": vehicle_state
    }


# ---------------------------------------------------------
# Functional correctness checks
# ---------------------------------------------------------

def check_vehicle_result(
    test_case,
    result
):
    if (
        test_case["category"]
        != "vehicle_command"
    ):
        return None

    expected_intent = (
        test_case.get(
            "expected_intent"
        )
    )

    predicted_intent = (
        result["predicted_intent"]
    )

    intent_correct = (
        predicted_intent
        == expected_intent
    )

    checks = {
        "intent_correct":
            intent_correct
    }

    vehicle_state = (
        result["vehicle_state"]
    )

    # -----------------------------------------------------
    # Temperature check
    # -----------------------------------------------------

    if "expected_temperature" in test_case:
        checks[
            "temperature_correct"
        ] = (
            vehicle_state[
                "temperature"
            ]
            == test_case[
                "expected_temperature"
            ]
        )

    # -----------------------------------------------------
    # Destination check
    # -----------------------------------------------------

    if "expected_destination" in test_case:
        checks[
            "destination_correct"
        ] = (
            vehicle_state[
                "destination"
            ]
            == test_case[
                "expected_destination"
            ]
        )

    return checks


# ---------------------------------------------------------
# Calculate evaluation summary
# ---------------------------------------------------------

def calculate_summary(
    all_results
):
    total_vehicle_tests = 0
    correct_vehicle_intents = 0

    total_unsupported_tests = 0
    correct_unsupported = 0

    baseline_times = []
    emotion_times = []

    for case in all_results:

        category = case["category"]

        baseline = (
            case["baseline"]
        )

        emotion_aware = (
            case["emotion_aware"]
        )

        baseline_times.append(
            baseline[
                "response_time_seconds"
            ]
        )

        emotion_times.append(
            emotion_aware[
                "response_time_seconds"
            ]
        )

        # -------------------------------------------------
        # Vehicle command accuracy
        # -------------------------------------------------

        if category == "vehicle_command":

            total_vehicle_tests += 1

            baseline_checks = (
                baseline[
                    "functional_checks"
                ]
            )

            emotion_checks = (
                emotion_aware[
                    "functional_checks"
                ]
            )

            # Count the test as correct only if both
            # Baseline and Emotion-Aware identify the
            # expected intent correctly.
            if (
                baseline_checks
                and baseline_checks.get(
                    "intent_correct",
                    False
                )
                and emotion_checks
                and emotion_checks.get(
                    "intent_correct",
                    False
                )
            ):
                correct_vehicle_intents += 1

        # -------------------------------------------------
        # Unsupported request detection
        # -------------------------------------------------

        if category == "unsupported":

            total_unsupported_tests += 1

            if (
                baseline[
                    "predicted_intent"
                ]
                == "unknown"
                and emotion_aware[
                    "predicted_intent"
                ]
                == "unknown"
            ):
                correct_unsupported += 1

    # -----------------------------------------------------
    # Calculate metrics
    # -----------------------------------------------------

    vehicle_accuracy = (
        correct_vehicle_intents
        / total_vehicle_tests
        if total_vehicle_tests
        else 0
    )

    unsupported_accuracy = (
        correct_unsupported
        / total_unsupported_tests
        if total_unsupported_tests
        else 0
    )

    average_baseline_time = (
        sum(baseline_times)
        / len(baseline_times)
        if baseline_times
        else 0
    )

    average_emotion_time = (
        sum(emotion_times)
        / len(emotion_times)
        if emotion_times
        else 0
    )

    return {
        "vehicle_intent_accuracy": round(
            vehicle_accuracy,
            4
        ),
        "unsupported_detection_accuracy": round(
            unsupported_accuracy,
            4
        ),
        "average_baseline_response_time": round(
            average_baseline_time,
            3
        ),
        "average_emotion_aware_response_time": round(
            average_emotion_time,
            3
        ),
        "total_test_cases": len(
            all_results
        ),
        "total_vehicle_tests":
            total_vehicle_tests,
        "correct_vehicle_intents":
            correct_vehicle_intents,
        "total_unsupported_tests":
            total_unsupported_tests,
        "correct_unsupported_requests":
            correct_unsupported
    }


# ---------------------------------------------------------
# Main evaluation
# ---------------------------------------------------------

def main():

    # -----------------------------------------------------
    # Load test cases
    # -----------------------------------------------------

    with open(
        TEST_CASES_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        test_cases = json.load(
            file
        )

    all_results = []

    print(
        "\nAVEMI EVALUATION"
    )

    print(
        "=" * 60
    )

    # -----------------------------------------------------
    # Run all test cases
    # -----------------------------------------------------

    for test_case in test_cases:

        print(
            f"\nRunning "
            f"{test_case['id']}"
        )

        case_result = {
            "id":
                test_case["id"],

            "category":
                test_case["category"],

            "emotion":
                test_case.get(
                    "emotion"
                ),

            "message":
                test_case["message"]
        }

        # ---------------------------------
        # Baseline evaluation
        # ---------------------------------

        baseline_result = run_case(
            test_case,
            "Baseline"
        )

        baseline_result[
            "functional_checks"
        ] = check_vehicle_result(
            test_case,
            baseline_result
        )

        # ---------------------------------
        # Emotion-Aware evaluation
        # ---------------------------------

        emotion_result = run_case(
            test_case,
            "Emotion-Aware"
        )

        emotion_result[
            "functional_checks"
        ] = check_vehicle_result(
            test_case,
            emotion_result
        )

        # ---------------------------------
        # Store results
        # ---------------------------------

        case_result[
            "baseline"
        ] = baseline_result

        case_result[
            "emotion_aware"
        ] = emotion_result

        all_results.append(
            case_result
        )

        # ---------------------------------
        # Terminal progress
        # ---------------------------------

        print(
            "  Baseline:"
        )

        print(
            f"    Intent: "
            f"{baseline_result['predicted_intent']}"
        )

        print(
            f"    Time: "
            f"{baseline_result['response_time_seconds']} s"
        )

        print(
            "  Emotion-Aware:"
        )

        print(
            f"    Intent: "
            f"{emotion_result['predicted_intent']}"
        )

        print(
            f"    Time: "
            f"{emotion_result['response_time_seconds']} s"
        )

    # -----------------------------------------------------
    # Calculate summary
    # -----------------------------------------------------

    summary = calculate_summary(
        all_results
    )

    # -----------------------------------------------------
    # Save results
    # -----------------------------------------------------

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "summary": summary,
                "results": all_results
            },
            file,
            indent=2
        )

    # -----------------------------------------------------
    # Print evaluation summary
    # -----------------------------------------------------

    print(
        "\nEVALUATION SUMMARY"
    )

    print(
        "=" * 60
    )

    print(
        f"Total test cases: "
        f"{summary['total_test_cases']}"
    )

    print(
        f"Vehicle intent accuracy: "
        f"{summary['vehicle_intent_accuracy'] * 100:.1f}%"
    )

    print(
        f"Unsupported request detection: "
        f"{summary['unsupported_detection_accuracy'] * 100:.1f}%"
    )

    print(
        f"Average baseline response time: "
        f"{summary['average_baseline_response_time']} s"
    )

    print(
        f"Average emotion-aware response time: "
        f"{summary['average_emotion_aware_response_time']} s"
    )

    print(
        "\nEvaluation complete."
    )

    print(
        f"Results saved to:\n"
        f"{RESULTS_FILE}"
    )


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()