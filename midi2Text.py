import pretty_midi
import argparse


def midi_to_text(midi_file, output_file):
    # Load MIDI file
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    # Process each instrument in the MIDI file
    with open(output_file, 'w') as file:
        for instrument in midi_data.instruments:
            # Get the instrument name using the program number and whether it's a drum track
            instrument_name = pretty_midi.program_to_instrument_name(
                instrument.program)
            if instrument.is_drum:
                instrument_name += " (Drum Kit)"

            # Process each note in the instrument
            prev_note = None
            for note in instrument.notes:
                # Get note name and octave
                note_name = pretty_midi.note_number_to_name(note.pitch)

                # Get note duration
                duration = note.end - note.start

                # Determine pitch direction
                if prev_note is None:
                    pitch_direction = "N/A"
                elif note.pitch > prev_note.pitch:
                    pitch_direction = "Up"
                elif note.pitch < prev_note.pitch:
                    pitch_direction = "Down"
                else:
                    pitch_direction = "Same"

                # Write note and instrument information to the output file
                file.write(f"Instrument: {instrument_name}\\n")
                file.write(f"Note: {note_name}\\n")
                file.write(f"Position: {note_name}\\n")
                file.write(f"Duration: {duration:.2f} seconds\\n")
                file.write(f"Pitch Direction: {pitch_direction}\\n")
                file.write("\\n")

                prev_note = note

    print(f"MIDI file converted to text. Output saved as '{output_file}'.")


# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Convert MIDI file to text representation.')
parser.add_argument('midi_file', type=str, help='Input MIDI file')
parser.add_argument('output_file', type=str, help='Output text file')
args = parser.parse_args()

# Call the function to convert MIDI to text
midi_to_text(args.midi_file, args.output_file)
