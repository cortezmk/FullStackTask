using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace calculation
{
    [Route("api/[controller]")]
    [ApiController]
    public class CalculationController : ControllerBase
    {
        [HttpPost] 
        public CalculationResult Post([FromBody] CalculationRequest request)
        {
            return new CalculationResult
            {
                Avg = request.Input.Average(),
                Sum = request.Input.Sum()
            };
        }
    }
}
