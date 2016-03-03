var GCD = 2.5;
var lastJudge = 12;

var skillSet = {
  '暖暖的微笑': Skill('暖暖的微笑', 0, 0, 10, true, function(player, ts) {
    if (!player.log['暖暖的微笑']) {
      player.log['暖暖的微笑'] = [];
    }
    player.log['暖暖的微笑'].push(ts);
    return true;
  }),
  '免疫挑剔': Skill('免疫挑剔', 0, 6, 9, true, function(player, ts) {
    player.immunes['挑剔的目光'] = ts + 6;
    return true;
  }),
  '挑剔的目光': Skill('挑剔的目光', 1.2, 0, 10, false, function(player, ts) {
    if (player.immunes['挑剔的目光'] && player.immunes['挑剔的目光'] >= ts) {
      return false;
    }
    if (player.reflect >= ts) {
      return false; // TODO: actual reflect
    }
    if (!player.log['挑剔的目光']) {
      player.log['挑剔的目光'] = 0;
    }
    player.log['挑剔的目光']++;
    return true;
  }),
  '迷人飞吻': Skill('迷人飞吻', 0, /* special */0, 18, true, function(player, ts) {
    if (!player.log['迷人飞吻']) {
      player.log['迷人飞吻'] = [];
    }
    player.log['迷人飞吻'].push(ts);
    return true;
  }),
  '圣诞礼物': Skill('圣诞礼物', 1.2, 6.5, 9, false, function(player, ts) {
    if (player.immunes['圣诞礼物'] && player.immunes['圣诞礼物'] >= ts) {
      return false;
    }
    if (!player.log['圣诞礼物']) {
      player.log['圣诞礼物'] = 0;
    }
    player.log['圣诞礼物']++;
    return ts <= lastJudge;
  }),
  '灰姑娘时钟': Skill('灰姑娘时钟', 1.2, 5.5, 11, false, function(player, ts) {
    if (player.immunes['灰姑娘时钟'] && player.immunes['灰姑娘时钟'] >= ts) {
      return false;
    }
    if (!player.log['灰姑娘时钟']) {
      player.log['灰姑娘时钟'] = 0;
    }
    player.log['灰姑娘时钟']++;
    return ts <= lastJudge;
  }),
  '免疫礼物': Skill('免疫礼物', 0, 4, 8, true, function(player, ts) {
    player.immunes['圣诞礼物'] = ts + 4;
    return true;
  }),
  '免疫灰姑娘': Skill('免疫灰姑娘', 0, 4, 10, true, function(player, ts) {
    player.immunes['灰姑娘时钟'] = ts + 4;
    return true;
  }),
  '沉睡魔咒': Skill('沉睡魔咒', 0.7, 5, 900, false, function(player, ts) {
    player.sleep = ts + 5;
    return true;
  }),
  '真爱之吻': Skill('真爱之吻', 0, 0, 900, true, function(player, ts) {
    player.sleep = ts;
    return true;
  }),
  '反弹挑剔': Skill('反弹挑剔', 0, 1.7, 900, true, function(player, ts) {
    player.reflect = ts + 1.7;
    return true;
  }),
  '短CD技能1': Skill('短CD技能1', 0, 0, 10, true, function(player, ts) {
    // do nothing
    return true;
  }),
  '短CD技能2': Skill('短CD技能2', 0, 0, 10, true, function(player, ts) {
    // do nothing
    return true;
  }),
};

function Skill(name, casting, duration, cd, isSelf, effect) {
  return {
    name: name,
    casting: casting,
    duration: duration,
    cd: cd,
    isSelf: isSelf,
    effect: effect
  };
}

function containsSkill(skills, name) {
  for (var i in skills) {
    if (skills[i].name == name) {
      return true;
    }
  }
  return false;
}

// Don't delete item, otherwise the length won't change
function deleteSkill(skills, name) {
  var ret = [];
  for (var i in skills) {
    if (skills[i].name != name) {
      ret.push(skills[i]);
    }
  }
  return ret;
}

function skillSuggestion(ememySkills) {
  var skills = [];
  // note: skills are put in orders
  skills.push(skillSet['暖暖的微笑']);
  if (containsSkill(ememySkills, "挑剔的目光")) {
    skills.push(skillSet['免疫挑剔']);
  }
  if (containsSkill(ememySkills, "圣诞礼物")) {
    skills.push(skillSet['免疫礼物']);
  }
  if (skills.length < 3 && containsSkill(ememySkills, "灰姑娘时钟")) {
    skills.push(skillSet['免疫灰姑娘']);
  }
  if (skills.length == 1) {
    skills.push(skillSet['短CD技能1']);
    skills.push(skillSet['短CD技能2']);
  } else if (skills.length == 2) {
    skills.push(skillSet['沉睡魔咒']); // thanks to 秋泠@tieba, the original all-purpose skill still works
  }
  skills.push(skillSet['迷人飞吻']);
  return skills;
}

function PlayerSkill() {
  return {
    skills: [],
    cd: {},
    put: function(skill) {
      this.skills.push(skill);
    },
    clear: function() {
      this.skills = [];
      this.cd = {};
    },
    use: function(skill, timestamp) {
      console.assert(containsSkill(this.skills, skill.name));
      console.assert(!this.cd[skill.name] || this.cd[skill.name] <= timestamp);
      for (var i in this.skills) {
        var s = this.skills[i];
        if (!this.cd[s.name]) {
          this.cd[s.name] = timestamp + GCD;
        } else {
          this.cd[s.name] = Math.max(this.cd[s.name], timestamp + GCD);
        }
      }
      this.cd[skill.name] = timestamp + skill.cd;
    },
    avail: function(timestamp) {
      var ret = [];
      for (var i in this.skills) {
        var skill = this.skills[i];
        if (!this.cd[skill.name] || this.cd[skill.name] <= timestamp) {
          ret.push(skill);
        }
      }
      return ret;
    }
  };
}

function EventBus() {
  return {
    events: {}, // heap would be a better choice, but why bother...
    put: function(skill, ts, isPlayer) {
      if (!this.events[ts]) {
        this.events[ts] = [];
      }
      this.events[ts].push([skill, isPlayer]);
    },
    nextTime: function() {
      var next = 18; // should be large enough
      for (var ts in this.events) {
        if (ts < next) {
          next = ts;
        }
      }
      return next;
    },
    use: function(player, enemy, ts) {
      if (this.events[ts]) {
        for (var i in this.events[ts]) {
          var skill = this.events[ts][i];
          var isPlayer = skill[1];
          if (isPlayer) {
            player.apply(skill[0], ts);
          } else {
            enemy.apply(skill[0], ts);
          }
        }
        delete this.events[ts];
      }
    }
  };
}
  
function Player(name, isPlayer) {
  return {
    name: name,
    skills: PlayerSkill(),
    isPlayer: isPlayer,
    summary: [],
    log: {},
    immunes: {},
    sleep: 0,
    use: function(skill, ts) {
      this.skills.use(skill, ts);
      this.summary.push(ts.toFixed(1) + "&nbsp;s: cast [" + skill.name + "]");
    },
    avail: function(ts) {
      var available = this.skills.avail(ts);
      if (this.sleep && this.sleep > ts) {
        var ret = [];
        if (containsSkill(available, '真爱之吻')) {
          ret.push(skillSet['真爱之吻']);
        }
        return ret;
      } else {
        return deleteSkill(available, '真爱之吻');
      }
    },
    apply: function(skill, ts) {
      var result = skill.effect(this, ts);
      if (result) {
        this.summary.push(ts.toFixed(1) + "&nbsp;s: get effect [" + skill.name + "]");
      }
    },
    nextTime: function() {
      var next = 18; // should be large enough
      for (var s in this.skills.cd) {
        var ts = this.skills.cd[s];
        if (s == '真爱之吻') {
          if (this.sleep <= 0) {
            ts = 18; // should be large enough
          }
        } else {
          ts = Math.max(this.sleep, ts);
        }
        if (ts < next) {
          next = ts;
        }
      }
      return next;
    }
  }
}