/*
  By Nicholas Riley, see
  http://stackoverflow.com/questions/784549/using-dictionary-apps-thesaurus-function-programmatically-on-osx-preferably-via

  compile with:
  gcc -o thesaurus -framework CoreServices -framework Foundation thesaurus.m
*/

#import <Foundation/Foundation.h>
#include <CoreServices/CoreServices.h>


int main(int argc, char *argv[]) {
  NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
  if (argc != 2) {
    puts([@"Usage: thesaurus WORD" UTF8String]);
    return 1;
  }
  NSUserDefaults *userDefaults = [NSUserDefaults standardUserDefaults];
  NSMutableDictionary *dictionaryPrefs =
    [[userDefaults persistentDomainForName:@"com.apple.DictionaryServices"] mutableCopy];

  NSArray *activeDictionaries = [dictionaryPrefs objectForKey:@"DCSActiveDictionaries"];

  [dictionaryPrefs setObject:
    [NSArray arrayWithObject:@"/Library/Dictionaries/Oxford American Writer's Thesaurus.dictionary"]
                      forKey:@"DCSActiveDictionaries"];
  [userDefaults setPersistentDomain:dictionaryPrefs forName:@"com.apple.DictionaryServices"];

  NSString *word = [NSString stringWithUTF8String:argv[1]];
  puts([(NSString *)DCSCopyTextDefinition(NULL, (CFStringRef)word,
                                          CFRangeMake(0, [word length])) UTF8String]);

  [dictionaryPrefs setObject:activeDictionaries forKey: @"DCSActiveDictionaries"];
  [userDefaults setPersistentDomain:dictionaryPrefs forName:@"com.apple.DictionaryServices"];
}