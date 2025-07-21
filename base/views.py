from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Answer, Guess, User
from .forms import GuessForm, UserForm     
import random


# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = User.objects.get(id=request.user.id)
    form = GuessForm(request.POST or None)
    answer = Answer.objects.first()
    guess = Guess.objects.filter(user=user)
    
    valid_guess = None

    if not answer:
        newGame(request)

    if request.method == 'POST':
        if form.is_valid():
            valid_guess = True
            new_guess = Guess.objects.create(
                user = user,
                word = request.POST.get('word'),
                attempt_number = Guess.objects.filter(user=user).count() + 1,
                result = evaluate_guess(request.POST.get('word'), answer.word)
            )

            guessed_letters = tuple(new_guess.word)
            user.guessed_letters.append(guessed_letters)
            flattened = [letter for guess in user.guessed_letters for letter in guess]
            user.guessed_letters = flattened
            user.save()

            if new_guess.word == answer.word:
                return redirect('win')
            elif guess.last().attempt_number == 6:
                return redirect('lose')
            
        else:
            valid_guess = False
        
    attempt = guess.last().attempt_number if guess else 0
    user_guesses = Guess.objects.filter(user=user).order_by('attempt_number')

    guess_rows = []
    result_rows = []
    for guess in user_guesses:
        guess_rows.append(tuple(guess.word))
        result_rows.append(tuple(guess.result))
    while len(guess_rows) < 6:
        guess_rows.append(('', '', '', '', ''))
        result_rows.append(('absent', 'absent', 'absent', 'absent', 'absent'))

    guess1 = guess_rows[0]
    guess2 = guess_rows[1]
    guess3 = guess_rows[2]
    guess4 = guess_rows[3]
    guess5 = guess_rows[4]
    guess6 = guess_rows[5]

    result1 = result_rows[0]
    result2 = result_rows[1]
    result3 = result_rows[2]
    result4 = result_rows[3]
    result5 = result_rows[4]
    result6 = result_rows[5]

    context_guess = {
               'guess1': guess1,
               'guess2': guess2,
               'guess3': guess3,
               'guess4': guess4,
               'guess5': guess5,
               'guess6': guess6,
    }

    context_result = {
               'result1': result1,
               'result2': result2,
               'result3': result3,
               'result4': result4,
               'result5': result5,
               'result6': result6,
    }

    context = {'user': user,
               'form': form, 
               'answer': answer,
               'attempt': attempt,
               'range_5': range(5),
               'valid_guess': valid_guess,
               **context_guess,
               **context_result}
    
    return render(request, 'base/home.html', context)


def evaluate_guess(guess, answer):
    result = ['absent'] * 5
    answer_chars = list(answer)
    guess_chars = list(guess)

    for i in range(5):
        if guess_chars[i] == answer_chars[i]:
            result[i] = 'exact'
            answer_chars[i] = None
            guess_chars[i] = None

        elif guess_chars[i] in answer_chars:
            result[i] = 'present'
            answer_chars[answer_chars.index(guess_chars[i])] = None

    return result


def registerPage(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')

    return render(request, 'base/register.html', {'form': form})


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Logged in")
            return redirect('home')
        else:
            print("Couldnt log in")
            messages.error(request, 'Incorrect username or password')

    context = {'page': page}
    return render(request, 'base/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def newGame(request):
    with open('allowed-guesses.txt') as f:
        valid_words = list(word.strip().upper() for word in f)

    answer = Answer.objects.first()

    if answer is None:
        answer = Answer.objects.create(
            word = random.choice(valid_words)
        )
    else:
        answer.word = random.choice(valid_words)
        answer.save()
    
    guess = Guess.objects.all()
    user = User.objects.get(id=request.user.id)
    user.guessed_letters = []
    user.rewarded = False
    user.save()
    for item in guess:
        item.delete()

    return redirect('home')


def win(request):
    user = User.objects.get(id=request.user.id)
    answer = Answer.objects.first()
    guess = Guess.objects.last()

    if user.rewarded == False:
        user.winstreak += 1
        user.rewarded = True

        if guess.attempt_number <= 2:
            user.score += 10 + (user.winstreak)
        elif guess.attempt_number <= 4:
            user.score += 7 + (user.winstreak)
        elif guess.attempt_number <= 6:
            user.score += 3 + (user.winstreak)

    user.save()

    context = {
        'user': user,
        'answer': answer,
        'guess': guess,
    }
    return render(request, 'base/win.html', context)

def lose(request):
    user = User.objects.get(id=request.user.id)
    answer = Answer.objects.first()

    user.winstreak = 0
    user.save()

    context = {
        'answer': answer
    }
    return render(request, 'base/lose.html', context)


def leaderboard(request):
    users = User.objects.all()

    context = {'users': users}
    return render(request, 'base/leaderboard.html', context)