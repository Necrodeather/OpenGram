from user.models import CustomUser


def save_subs(
    profile: CustomUser,
    follower: CustomUser,
    added: bool = True,
) -> None:
    if added:
        profile.followers += 1
        follower.following += 1
    else:
        profile.followers -= 1
        follower.following -= 1
    users = [profile, follower]
    CustomUser.objects.bulk_update(
        users,
        ["followers", "following"],
        batch_size=2,
    )
