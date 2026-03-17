"""
ARS Pharma Virtual Sales Rep Assistant
Internal use only — supports ARS sales reps with PA workflows, talk tracks,
call prep guidance, and next best actions.
"""

import os
import anthropic

SYSTEM_PROMPT = """You are an internal ARS Pharma Virtual Sales Rep Assistant. Your purpose is to SUPPORT ARS sales reps and virtual sales reps by:
• Answering questions about prior authorization (PA), formulary exception workflows, and office process navigation
• Providing rep-ready talk tracks, checklists, and call preparation guidance
• Helping reps summarize calls and identify next best actions

STRICT BOUNDARIES:
• You are for INTERNAL USE ONLY.
• You do NOT communicate directly with HCPs, nurses, patients, or offices.
• You do NOT send emails, place calls, or generate external communications without explicit human approval.
• You do NOT provide medical advice, prescribing guidance, or clinical recommendations.
• You do NOT guarantee coverage, approval, or reimbursement outcomes.

KNOWLEDGE & GROUNDING:
• You must answer ONLY using the approved internal knowledge sources provided (e.g., Market Access / PA training materials).
• If information is not found in the provided sources, clearly say: "I don't have that information in the approved materials. I recommend escalating to Market Access or PA support."
• Do not guess, invent policies, or hallucinate answers.

OUTPUT STYLE:
• Be clear, concise, and operational.
• Use bullets and step-by-step checklists when helpful.
• When appropriate, structure responses as:
  – "What to say"
  – "What to ask the office"
  – "What to do next"

ESCALATION RULES:
• If the question involves:
  – Patient-specific data
  – Clinical judgment
  – Coverage guarantees
  – Policy interpretation beyond training materials
  Then immediately recommend escalation to a human ARS contact.

HUMAN-IN-THE-LOOP REMINDER:
• All outputs must be reviewed and validated by an ARS employee before use.
• Treat your responses as drafts and decision support, not final authority.

TONE:
• Professional, compliant, and supportive
• Confident but conservative
• Never speculative

If the user asks something outside your scope, explain the limitation and redirect appropriately."""


def create_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY environment variable is not set. "
            "Please set it before running the assistant."
        )
    return anthropic.Anthropic(api_key=api_key)


def run_assistant():
    """Run the ARS Pharma Virtual Sales Rep Assistant as an interactive CLI."""
    client = create_client()
    conversation: list[dict] = []

    print("=" * 60)
    print("ARS Pharma Virtual Sales Rep Assistant")
    print("INTERNAL USE ONLY — For ARS Sales Reps")
    print("=" * 60)
    print("Type your question below. Type 'quit' or 'exit' to end.")
    print("All responses are drafts — review before use.\n")

    while True:
        try:
            user_input = input("Rep: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSession ended.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Session ended. Remember to review all outputs before use.")
            break

        conversation.append({"role": "user", "content": user_input})

        try:
            with client.messages.stream(
                model="claude-opus-4-6",
                max_tokens=2048,
                system=SYSTEM_PROMPT,
                messages=conversation,
                thinking={"type": "adaptive"},
            ) as stream:
                print("\nAssistant: ", end="", flush=True)
                full_response = ""
                for text in stream.text_stream:
                    print(text, end="", flush=True)
                    full_response += text
                print("\n")

            conversation.append({"role": "assistant", "content": full_response})

        except anthropic.AuthenticationError:
            print("\nError: Invalid API key. Please check your ANTHROPIC_API_KEY.\n")
            break
        except anthropic.RateLimitError:
            print("\nRate limit reached. Please wait a moment and try again.\n")
            conversation.pop()
        except anthropic.APIError as e:
            print(f"\nAPI error ({e.status_code}): {e.message}\n")
            conversation.pop()


def get_single_response(user_message: str, history: list[dict] | None = None) -> str:
    """
    Programmatic interface: send a single message and return the assistant response.

    Args:
        user_message: The rep's question or request.
        history: Optional prior conversation turns for multi-turn context.

    Returns:
        The assistant's response text.
    """
    client = create_client()
    messages = list(history or [])
    messages.append({"role": "user", "content": user_message})

    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=messages,
        thinking={"type": "adaptive"},
    ) as stream:
        return stream.get_final_message().content[0].text


if __name__ == "__main__":
    run_assistant()
