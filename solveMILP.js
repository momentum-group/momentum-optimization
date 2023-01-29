
exports = async function(company_name){
    const users = await context.services.get("mongodb-atlas").db("org_companyName").collection("users").find({company: 'AIDED', is_employer: false});
    const usersArray = await users.toArray();
    
    const company = await context.services.get("mongodb-atlas").db("org_companyName").collection("employer").findOne({company: company_name});
    
    var transposed = {
      firstname: [],
      max_hours: [],
      min_hours: [],
      preferred_hours: [],
      people: [],
      needed_capacity: []
    }
    
    for (let i = 0; i < usersArray.length; i++) {
      const user = JSON.parse(JSON.stringify(usersArray[i]));
      // console.log(user._id);
      transposed['firstname'].push(user.firstname);
      transposed['max_hours'].push(user.max_hours);
      transposed['min_hours'].push(user.min_hours);
      transposed['preferred_hours'].push(user.preferred_hours);
      transposed['people'].push(user.availability); // bad name. Should have been called availability
    }
    
    transposed['needed_capacity'] = company.needed_capacity
    
    // transposed = {
    //   max_hours: [5, 5],
    //   min_hours: [1, 1],
    //   preferred_hours: [5, 4],
    //   people: [[0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    //         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]],
    //   needed_capacity: [1, 1, 1, 2, 2, 2, 2, 1, 1, 0, 0]
    // }
    
    console.log(JSON.stringify(transposed));
    
    // return response;
    const response = await context.http.post({
      url: "http://104.248.109.231:5000/schedule",
      body: JSON.stringify(transposed)
    })
    if (response.status == '500 INTERNAL SERVER ERROR'){
      return 500;
    } else {
      const milp_solution = JSON.parse(response.body.text());
      if (milp_solution.status == 'Optimal'){
        //update database
        console.log(JSON.stringify(milp_solution))
        var date = new Date();
        
        for (let i = 0; i < transposed['firstname'].length; i++) {
          console.log(milp_solution.result[i]);
          context.services.get("mongodb-atlas").db("org_companyName").collection("users").updateOne({'firstname': transposed['firstname'][i]}, {$set: {'result.createdAt': date, 'result.schedule': milp_solution.result[i]}}, {$upsert: true});
        }
        return 'Optimal';
      } else if (milp_solution.status == 'Infeasible'){
        return 'Infeasible';
      } else {
        return milp_solution
      }
    }
  };