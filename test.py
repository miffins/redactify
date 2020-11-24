
import redactifier

redactedText, names = redactifier.redactAllNames(open("sampleText/economists.txt", "r").read())

print(redactedText)
print("\nContained " + len(names) + " instances of the following names:")
print(sorted(set(names)))