import sys
import speech_recognition as sr
from agent import VoiceAgent
from config import GROQ_MODEL

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    console = Console()
    USE_RICH = True
except ImportError:
    USE_RICH = False


def print_banner():
    if USE_RICH:
        banner = (
            f"[bold cyan]🎙️ Production Voice AI Agent[/bold cyan]\n"
            f"[dim]Real-Time Conversational Loop: STT -> Groq LPU ({GROQ_MODEL}) -> Local TTS[/dim]\n"
            f"[yellow]Features:[/yellow] Multi-turn context | Latency logging | Adaptive noise calibration\n"
            f"[dim]Say [bold]'exit'[/bold], [bold]'quit'[/bold], or [bold]'bye'[/bold] to terminate session.[/dim]"
        )
        console.print(Panel(banner, border_style="cyan", expand=False))
    else:
        print("=" * 60)
        print("🎙️ Production Voice AI Agent")
        print(f"Model: {GROQ_MODEL} | Multi-turn Voice Dialogue")
        print("Say 'exit', 'quit', or 'bye' to terminate.")
        print("=" * 60)


def run():
    agent = VoiceAgent()
    print_banner()

    try:
        with sr.Microphone() as source:
            if USE_RICH:
                with console.status("[dim yellow]Calibrating microphone for ambient room noise...[/dim yellow]"):
                    agent.stt.calibrate(source)
                console.print("[bold green]✓ Microphone calibrated and ready.[/bold green]\n")
            else:
                print("Calibrating microphone for ambient noise...")
                agent.stt.calibrate(source)
                print("✓ Microphone ready.\n")

            while True:
                try:
                    if USE_RICH:
                        console.print("[dim cyan]Listening... Speak into your microphone:[/dim cyan]")
                    else:
                        print("Listening...")

                    user_text = agent.stt.listen_and_transcribe(source)

                    if not user_text:
                        continue

                    # Display user speech
                    if USE_RICH:
                        console.print(f"[bold white]You:[/bold white] [bold cyan]{user_text}[/bold cyan]")
                    else:
                        print(f"You: {user_text}")

                    # Exit check
                    if agent.is_exit_command(user_text):
                        farewell = "Goodbye! Have a wonderful day!"
                        if USE_RICH:
                            console.print(f"[bold green]AI:[/bold green] {farewell}")
                        else:
                            print(f"AI: {farewell}")
                        agent.tts.speak(farewell)
                        break

                    # Process turn with latency display
                    def on_response(ai_text: str, latency: float):
                        if USE_RICH:
                            header = f"[bold green]AI Assistant[/bold green] [dim]({latency*1000:.0f}ms latency)[/dim]"
                            console.print(Panel(Markdown(ai_text), title=header, border_style="green"))
                        else:
                            print(f"AI ({latency*1000:.0f}ms): {ai_text}")

                    agent.process_turn(user_text, on_response=on_response)

                except KeyboardInterrupt:
                    print("\nVoice session ended.")
                    break
                except RuntimeError as err:
                    if USE_RICH:
                        console.print(f"[bold red]Service Error:[/bold red] {err}")
                    else:
                        print(f"Service Error: {err}")
                    break

    except AttributeError:
        print("\n[Error] PyAudio is not installed or microphone not found.")
        print("Install PyAudio with: pip install pyaudio")
    except Exception as e:
        print(f"\n[Fatal Error]: {e}")


if __name__ == "__main__":
    run()
